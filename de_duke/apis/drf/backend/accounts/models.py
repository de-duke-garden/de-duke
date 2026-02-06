from fileinput import filename
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.hashers import make_password, check_password
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
import random
import uuid
import string
from django.conf import settings
import os
from django.utils.deconstruct import deconstructible
import boto3
import logging

from utilities import idx

logger = logging.getLogger("django")


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        # if os.getenv("DJANGO_SETTINGS_MODULE") == "main.settings.aws":
        #     cognito_client = boto3.client("cognito-idp")
        #     cognito_user = cognito_client.admin_create_user(
        #         UserPoolId=settings.COGNITO_USER_POOL,
        #         Username=email,
        #         TemporaryPassword=password,
        #         UserAttributes=[
        #             {
        #                 'Name': 'email',
        #                 'Value': email
        #             },
        #             {
        #                 'Name': 'given_name',
        #                 'Value': extra_fields.get('first_name')
        #             },
        #             {
        #                 'Name': 'family_name',
        #                 'Value': extra_fields.get('last_name')
        #             }
        #         ]
        #     )
        #     for attribute in cognito_user['User']['Attributes']:
        #         if attribute['Name'] == 'sub':
        #             user.cognito_uid = attribute['Value']
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    User model class
    """

    id = models.CharField(
        _("ID"),
        primary_key=True,
        max_length=255,
        default=idx.generate_user_id,
        editable=False,
    )
    username = None
    email = models.EmailField(_("email address"), unique=True)
    email_verified = models.BooleanField(
        _("email verified"),
        default=False,
        help_text=_("Designates whether the email has been verified."),
    )
    firebase_uid = models.CharField(max_length=255, unique=True, null=True, blank=True)
    cognito_uid = models.CharField(max_length=255, unique=True, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["first_name"]

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def has_google_account(self):
        return self.firebase_uid is not None

    def has_cognito_account(self):
        return self.cognito_uid is not None

    def has_phone_number(self):
        try:
            return self.phone_number is not None and self.phone_number.is_verified
        except User.phone_number.RelatedObjectDoesNotExist:
            return False

    def is_host(self):
        try:
            return self.host_account.exists()
        except Exception as e:
            logger.error(e)
            return False

    def verified_host_account(self):
        return self.host_account.filter(status="verified").first()

    def is_host_verified(self):
        """
        Check if the user is a verified host.
        """
        try:
            return self.host_account.filter(status="verified").exists()
        except Exception as e:
            logger.error(e)
            return False

    def host_status(self):
        if self.is_host():
            return self.host_account.order_by("-created_at").first().status
        return None

    def host_status_reason(self):
        if self.is_host():
            return self.host_account.order_by("-created_at").first().status_reason
        return None

    def get_or_create_for_cognito(self, jwt_payload):
        try:
            return User.objects.get(
                Q(email=jwt_payload["email"]) | Q(cognito_uid=jwt_payload["sub"])
            )
        except User.DoesNotExist:
            user = User.objects.create_user(
                email=jwt_payload["email"],
                password=None,
                first_name=jwt_payload["given_name"],
                last_name=jwt_payload["family_name"],
                cognito_uid=jwt_payload["sub"],
            )
            return user


class TimeStampedBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class OTPRequest(TimeStampedBaseModel):
    id = models.CharField(
        primary_key=True, max_length=255, default=idx.generate_otp_id, editable=False
    )
    ref = models.TextField()
    # Hashed random token for device identity
    device_identity = models.CharField(max_length=255)
    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(
        default=False, help_text=_("Designates whether the OTP has been verified.")
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("OTP Request")
        verbose_name_plural = _("OTP Requests")

    def __str__(self):
        return f"{self.ref} - {self.otp}"

    # THE DEVICE IDENTITY IS TO ENSURE THAT THE DEVICE THAT REQUESTED THE OTP IS THE SAME DEVICE THAT IS VERIFYING IT.
    # THIS IS TO PREVENT OTP REUSE ATTACKS.

    def has_expired(self):
        """
        Check if the OTP request has expired based on the expiration time.
        """
        expiration_time = timezone.timedelta(
            seconds=getattr(settings, "OTP_EXPIRATION_TIME", 600)
        )
        return timezone.now() > self.created_at + expiration_time

    def is_device_valid(self, device_identity):
        """
        Validate the provided device identity against the stored device identity.
        """
        return check_password(device_identity, self.device_identity)

    def is_valid(self, device_identity):
        """
        Check if the OTP request can be verified:
        - The device identity token is valid.
        - The OTP request has not expired.
        """
        return self.is_device_valid(device_identity) and not self.has_expired()

    @staticmethod
    def generate_otp():
        """
        Generate a 6-digit OTP.
        """
        return f"{random.randint(100000, 999999)}"

    @staticmethod
    def generate_device_token(length=10):
        """
        Generate a hashed random string to be used as a device identity token.
        """
        characters = string.ascii_letters + string.digits
        plain_token = "".join(random.choice(characters) for _ in range(length))
        hashed_token = make_password(plain_token)
        return hashed_token, plain_token


class PhoneNumber(TimeStampedBaseModel):
    """
    PhoneNumber model class
    """

    id = models.CharField(
        primary_key=True,
        max_length=255,
        default=idx.generate_phone_number_id,
        editable=False,
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="phone_number"
    )
    mobile = models.CharField(max_length=15, unique=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Phone Number")
        verbose_name_plural = _("Phone Numbers")


def upload_identity_image(instance, filename: str):
    # Use the user's ID and the original filename to create a unique path
    root, ext = os.path.splitext(filename)
    # support only 1 upload/hosts
    return f"identities/{instance.user.email}.{ext}"


@deconstructible
class UploadHostAccountHelper:
    def __init__(self, field_name):
        self.field_name = field_name

    def __call__(self, instance, filename: str):
        root, ext = os.path.splitext(filename)
        return f"hosts/{instance.user.id}/{self.field_name}.{ext}"


class HostAccount(TimeStampedBaseModel):
    HOST_ACCOUNT_TYPE_CHOICES = [
        ("agent", "Agent"),
        ("architect", "Architect"),
        ("company", "Company"),
        ("lawyer", "Lawyer"),
        ("owner", "Owner"),
        ("surveyor", "Surveyor"),
    ]
    HOST_ACCOUNT_STATUS_CHOICES = [
        ("verified", "Verified"),
        ("rejected", "Rejected"),
        ("in_review", "In Review"),
    ]
    id = models.CharField(
        primary_key=True, max_length=255, default=idx.generate_host_id, editable=False
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="host_account"
    )
    # is_verified = models.BooleanField(default=False, help_text=_(
    #     "Designates whether the host account has been verified."))

    status = models.CharField(
        _("Verification Status"),
        max_length=100,
        help_text=_("Verification status"),
        choices=HOST_ACCOUNT_STATUS_CHOICES,
        default="in_review",
    )
    status_reason = models.TextField(
        _("Verification Status Reason"),
        null=True,
        blank=True,
    )
    host_photo = models.ImageField(
        _("Host Photo"),
        upload_to=UploadHostAccountHelper("host_photo"),
        max_length=255,
    )
    bio = models.TextField(
        _("Host Bio"),
        max_length=500,
        help_text=_("A brief bio about the host."),
        blank=True,
    )
    # identity_number = models.CharField(
    #     _("Identity Number"), max_length=100, unique=True, help_text=_("Unique number for the identity.")
    # )
    type = models.CharField(
        _("Host Type"),
        max_length=100,
        help_text=_("Type of host, e.g., lawyer, agent, etc."),
        choices=HOST_ACCOUNT_TYPE_CHOICES,
        blank=True,
        null=True,
    )

    def is_verified(self):
        return self.status == "verified"

    def clean(self):
        super().clean()
        # Only perform checks when creating a new instance
        if self._state.adding:
            verified_inst = (
                HostAccount.objects.filter(status="verified", user=self.user)
                .order_by("-created_at")
                .first()
            )
            if verified_inst is not None:
                raise ValidationError(
                    f"Host account is already verified as a {verified_inst.type}"
                )
            inst = (
                HostAccount.objects.filter(user=self.user)
                .order_by("-created_at")
                .first()
            )
            if inst is not None and inst.status == "in_review":
                raise ValidationError(f"Host account is in review as a {inst.type}")

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        # Ensure clean() is called before saving
        self.full_clean()

        # Build kwargs for parent save() call
        save_kwargs = {"using": using, "update_fields": update_fields}
        if force_insert:
            save_kwargs["force_insert"] = force_insert
        if force_update:
            save_kwargs["force_update"] = force_update

        return super().save(**save_kwargs)

    def __str__(self):
        return f"{self.user.email} ({self.type}) - {self.status}"

    class Meta:
        verbose_name = _("Host Account")
        verbose_name_plural = _("Host Accounts")


class HostAccountLawyer(HostAccount):
    nba_enrol_no = models.CharField(
        _("NBA Enrollment Number"),
        max_length=100,
        unique=True,
        help_text=_("NBA Enrollment Number for the lawyer host."),
    )
    # TODO: Change to practice_license
    valid_practicing_cert = models.ImageField(
        _("Valid Practicing Certificate"),
        upload_to=UploadHostAccountHelper("valid_practicing_cert"),
        max_length=255,
    )
    govt_issued_id = models.ImageField(
        _("Government Issued ID"),
        upload_to=UploadHostAccountHelper("govt_issued_id"),
        max_length=255,
    )
    proof_of_address = models.ImageField(
        _("Proof of Address"),
        upload_to=UploadHostAccountHelper("proof_of_address"),
        max_length=255,
    )
    ref_phone_no = models.CharField(
        _("Reference Phone Number"),
        max_length=15,
        help_text=_("Reference Phone Number for the lawyer host."),
    )

    def __str__(self):
        return f"{self.user.email} - ({'Is verified' if self.is_verified else 'Not verified'})"

    def save(self, *args, **kwargs):
        self.type = "lawyer"
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Lawyer's Host Account")
        verbose_name_plural = _("Lawyer's Host Accounts")


class HostAccountArchitect(HostAccount):
    arcon_reg_no = models.CharField(
        _("ARCON Registration Number"),
        max_length=100,
        unique=True,
        help_text=_("ARCON Registration Number for the architect host."),
    )
    practice_license = models.ImageField(
        _("Practice License"),
        upload_to=UploadHostAccountHelper("practice_license"),
        max_length=255,
    )
    govt_issued_id = models.ImageField(
        _("Government Issued ID"),
        upload_to=UploadHostAccountHelper("govt_issued_id"),
        max_length=255,
    )
    ref_phone_no = models.CharField(
        _("Reference Phone Number"),
        max_length=15,
        help_text=_("Reference Phone Number for the architect host."),
    )

    def __str__(self):
        return f"{self.user.email} - ({'Is verified' if self.is_verified else 'Not verified'})"

    def save(self, *args, **kwargs):
        self.type = "architect"
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Architect's Host Account")
        verbose_name_plural = _("Architect's Host Accounts")


class HostAccountSurveyor(HostAccount):
    surcon_reg_no = models.CharField(
        _("SURCON Registration Number"),
        max_length=100,
        unique=True,
        help_text=_("SURCON Registration Number for the surveyor host."),
    )
    practice_license = models.ImageField(
        _("Practice License"),
        upload_to=UploadHostAccountHelper("practice_license"),
        max_length=255,
    )
    govt_issued_id = models.ImageField(
        _("Government Issued ID"),
        upload_to=UploadHostAccountHelper("govt_issued_id"),
        max_length=255,
    )
    ref_phone_no = models.CharField(
        _("Reference Phone Number"),
        max_length=15,
        help_text=_("Reference Phone Number for the surveyor host."),
    )

    def __str__(self):
        return f"{self.user.email} - ({'Is verified' if self.is_verified else 'Not verified'})"

    def save(self, *args, **kwargs):
        self.type = "surveyor"
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Surveyor's Host Account")
        verbose_name_plural = _("Surveyor's Host Accounts")


class HostAccountCompany(HostAccount):
    cac_reg_doc = models.ImageField(
        _("CAC Registration Document"),
        upload_to=UploadHostAccountHelper("cac_reg_doc"),
        max_length=255,
    )
    proof_of_address = models.ImageField(
        _("Proof of Address"),
        upload_to=UploadHostAccountHelper("proof_of_address"),
        max_length=255,
    )
    rep_id = models.ImageField(
        _("Dir./Authorized Rep. ID Number"),
        upload_to=UploadHostAccountHelper("rep_id"),
        max_length=255,
    )

    def __str__(self):
        return f"{self.user.email} - ({'Is verified' if self.is_verified else 'Not verified'})"

    def save(self, *args, **kwargs):
        self.type = "company"
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Company Host Account")
        verbose_name_plural = _("Company Host Accounts")


class HostAccountAgent(HostAccount):
    cac_cert_doc = models.ImageField(
        _("CAC Certificate Document"),
        upload_to=UploadHostAccountHelper("cac_cert_doc"),
        max_length=255,
    )
    industry_license = models.ImageField(
        _("Industry License"),
        upload_to=UploadHostAccountHelper("industry_license"),
        max_length=255,
        blank=True,
        null=True,
    )
    proof_of_address = models.ImageField(
        _("Proof of Address"),
        upload_to=UploadHostAccountHelper("proof_of_address"),
        max_length=255,
    )
    rep_id = models.ImageField(
        _("Dir./Authorized Rep. ID Number"),
        upload_to=UploadHostAccountHelper("rep_id"),
        max_length=255,
    )

    def __str__(self):
        return f"{self.user.email} - ({'Is verified' if self.is_verified else 'Not verified'})"

    def save(self, *args, **kwargs):
        self.type = "agent"
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Agent Host Account")
        verbose_name_plural = _("Agent Host Accounts")


class HostAccountOwner(HostAccount):
    def __str__(self):
        return f"{self.user.email} - ({'Is verified' if self.is_verified else 'Not verified'})"

    def save(self, *args, **kwargs):
        self.type = "owner"
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Owner Host Account")
        verbose_name_plural = _("Owner Host Accounts")
