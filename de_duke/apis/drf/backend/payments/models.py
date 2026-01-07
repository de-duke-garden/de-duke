from django.db import models
from properties.models import Property
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
        ('initiated', 'Initiated'),
        ('successful', 'Successful'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    PAYMENT_GATEWAY_CHOICES = [
        ('flutterwave', 'Flutterwave'),
        ('paystack', 'Paystack'),
    ]

    id = models.CharField(
        primary_key=True,
        editable=False,
        max_length=255,
        default=idx.generate_checkout_id,
        help_text="An identifier for the checkout session. Default is a {idx.generate_checkout_id}."
    )
    unit_amount = models.IntegerField(
        help_text="Amount in the smallest currency unit",
        default=0
    )
    currency = models.CharField(max_length=10, default='NGN')
    reference = models.CharField(
        max_length=255, unique=True, null=True, blank=True)
    payment_gateway = models.CharField(
        max_length=100, choices=PAYMENT_GATEWAY_CHOICES)
    status = models.CharField(
        max_length=50, choices=PAYMENT_STATUS_CHOICES, default='initiated')
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
        Property, on_delete=models.CASCADE, related_name="property_checkouts")
    user = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT, related_name="property_checkouts")

    class Meta:
        verbose_name = "Property Checkout"
        verbose_name_plural = "Property Checkouts"
        ordering = ["-created_at"]
