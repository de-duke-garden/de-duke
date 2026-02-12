from rest_framework import serializers
from .models import (
    HostAccountAgent,
    HostAccountArchitect,
    HostAccountCompany,
    HostAccountLawyer,
    HostAccountOwner,
    HostAccountSurveyor,
    User,
    PhoneNumber,
)


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new user.
    It includes fields for email, password, and phone number.
    """

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="get_full_name", read_only=True)
    is_host_verified = serializers.BooleanField(read_only=True)
    is_admin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "is_active",
            "is_admin",
            "date_joined",
            "is_host_verified",
        ]
        read_only_fields = ["id", "date_joined", "is_active", "is_admin"]

    def get_is_admin(self, obj) -> bool:
        return obj.is_superuser or obj.is_staff


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ["mobile", "is_verified"]
        read_only_fields = ["is_verified"]


class UserMeSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberSerializer(required=False, read_only=True)
    is_host = serializers.BooleanField(read_only=True)
    is_host_verified = serializers.BooleanField(read_only=True)
    host_status = serializers.CharField(
        allow_null=True, allow_blank=True, read_only=True
    )
    host_status_reason = serializers.CharField(
        allow_null=True, allow_blank=True, read_only=True
    )

    class Meta:
        model = User
        exclude = [
            "password",
            "is_superuser",
            "is_staff",
            "firebase_uid",
            "cognito_uid",
        ]
        read_only_fields = [
            "id",
            "date_joined",
            "last_login",
            "is_active",
            "is_staff",
            "is_superuser",
            "email_verified",
            "email",
            "groups",
            "user_permissions",
        ]


class ChangeAccountPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()


class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    device_identity = serializers.CharField(max_length=255)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(min_length=6)
    device_identity = serializers.CharField(max_length=255)


class ResetPasswordWithTokenSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=6)


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    device_identity = serializers.CharField(max_length=255)


class VerifyEmailWithTokenSerializer(serializers.Serializer):
    token = serializers.CharField()


class BecomeAHostAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostAccountAgent
        exclude = ["user", "type", "created_at", "updated_at"]
        read_only_fields = [
            "id",
            "status",
            "status_reason",
            "is_verified",
            "created_at",
            "updated_at",
        ]


class BecomeAHostArchitectSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostAccountArchitect
        exclude = ["user", "type", "created_at", "updated_at"]
        read_only_fields = [
            "id",
            "status",
            "status_reason",
            "is_verified",
            "created_at",
            "updated_at",
        ]


class BecomeAHostCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = HostAccountCompany
        exclude = ["user", "type", "created_at", "updated_at"]
        read_only_fields = [
            "id",
            "status",
            "status_reason",
            "is_verified",
            "created_at",
            "updated_at",
        ]


class BecomeAHostLawyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostAccountLawyer
        exclude = ["user", "type", "created_at", "updated_at"]
        read_only_fields = [
            "id",
            "status",
            "status_reason",
            "is_verified",
            "created_at",
            "updated_at",
        ]


class BecomeAHostOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostAccountOwner
        exclude = ["user", "type", "created_at", "updated_at"]
        read_only_fields = [
            "id",
            "status",
            "status_reason",
            "is_verified",
            "created_at",
            "updated_at",
        ]


class BecomeAHostSurveyorSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostAccountSurveyor
        exclude = ["user", "type", "created_at", "updated_at"]
        read_only_fields = [
            "id",
            "status",
            "status_reason",
            "is_verified",
            "created_at",
            "updated_at",
        ]
