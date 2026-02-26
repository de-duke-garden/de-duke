from django.db import models
from django.core.exceptions import ValidationError
from properties.models import Property, PropertyChat
from django.contrib.auth import get_user_model
from django.utils import timezone
from utilities import idx


# class Payment(models.Model):
#     id = models.CharField(
#         primary_key=True,
#         editable=False,
#         default=idx.generate_payment_id,
#         max_length=255,
#         help_text="Payment ID",
#     )
#     unit_amount = models.IntegerField(
#         help_text="Amount in the smallest currency unit"
#     )
#     currency = models.CharField(max_length=10, default='NGN')
#     reference = models.CharField(max_length=255, unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def amount(self):
#         return self.unit_amount / 100.0

#     def __str__(self):
#         return f"{self.checkout.payment_gateway} - {self.currency}{self.amount()}"


class Checkout(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ("initiated", "Initiated"),
        ("successful", "Successful"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
    ]
    PAYMENT_GATEWAY_CHOICES = [
        ("flutterwave", "Flutterwave"),
        ("paystack", "Paystack"),
    ]

    id = models.CharField(
        primary_key=True,
        editable=False,
        max_length=255,
        default=idx.generate_checkout_id,
        help_text="An identifier for the checkout session. Default is a {idx.generate_checkout_id}.",
    )
    unit_amount = models.IntegerField(
        help_text="Amount in the smallest currency unit", default=0
    )
    currency = models.CharField(max_length=10, default="NGN")
    reference = models.CharField(max_length=255, unique=True, null=True, blank=True)
    payment_gateway = models.CharField(max_length=100, choices=PAYMENT_GATEWAY_CHOICES)
    status = models.CharField(
        max_length=50, choices=PAYMENT_STATUS_CHOICES, default="initiated"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def amount(self):
        return self.unit_amount / 100.0

    def __str__(self):
        return f"{self.payment_gateway} - {self.currency}{self.amount()}"

    class Meta:
        abstract = True
        verbose_name = "Checkout"
        verbose_name_plural = "Checkouts"
        ordering = ["-created_at"]


class PropertyCheckout(Checkout):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="property_checkouts"
    )
    user = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT, related_name="property_checkouts"
    )

    class Meta:
        verbose_name = "Property Checkout"
        verbose_name_plural = "Property Checkouts"
        ordering = ["-created_at"]


class Invoice(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ("initiated", "Initiated"),
        # ("pending", "Pending"),
        ("successful", "Successful"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
    ]
    PAYMENT_GATEWAY_CHOICES = [
        ("flutterwave", "Flutterwave"),
        ("paystack", "Paystack"),
    ]

    id = models.CharField(
        primary_key=True,
        editable=False,
        max_length=255,
        default=idx.generate_invoice_id,
        help_text="An identifier for the invoice. Default is a {idx.generate_invoice_id}.",
    )
    unit_amount = models.IntegerField(
        help_text="Amount in the smallest currency unit", default=0
    )
    currency = models.CharField(max_length=10, default="NGN")
    reference = models.CharField(max_length=255, unique=True, null=True, blank=True)
    payment_gateway = models.CharField(max_length=100, choices=PAYMENT_GATEWAY_CHOICES)
    status = models.CharField(
        max_length=50, choices=PAYMENT_STATUS_CHOICES, default="initiated"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def amount(self):
        return self.unit_amount / 100.0

    @property
    def is_paid(self):
        return self.status == "successful"

    def __str__(self):
        return f"{self.payment_gateway} - {self.currency}{self.amount()}"

    class Meta:
        abstract = True
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"
        ordering = ["-created_at"]


class PropertyChatInvoice(Invoice):
    property_chat = models.ForeignKey(
        PropertyChat, on_delete=models.CASCADE, related_name="property_chat_invoices"
    )
    is_sealed = models.BooleanField(default=False)
    possession_period_start_date = models.DateTimeField(null=False, blank=False)
    possession_period_end_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Property Chat Invoice"
        verbose_name_plural = "Property Chat Invoices"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        # if invoice is sealed, disable further updates
        # if kwargs.get("is_sealed") is True:
        #     raise ValidationError("Invoice is sealed and cannot be updated")
        if not self._state.adding:
            old_inst = PropertyChatInvoice.objects.get(pk=self.pk)
            if old_inst.status != "initiated":
                raise ValidationError("Invoice has already been proccessed")
        if not self.property_chat.property.is_open_for_invoice:
            raise ValidationError("Property is not open for invoice")

        # if possession period is set on property, set the possession period end date to that many days from the start date
        if (
            self.possession_period_start_date
            and self.property_chat.property.possession_period_days
        ):
            self.possession_period_end_date = (
                self.possession_period_start_date
                + timezone.timedelta(
                    days=self.property_chat.property.possession_period_days
                )
            )
        super().save(*args, **kwargs)
