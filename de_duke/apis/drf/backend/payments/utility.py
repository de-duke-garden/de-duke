from properties.models import Property
from utilities import idx
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import requests
import paystack

from .models import PropertyCheckout, PropertyChatInvoice


User = get_user_model()
paystack.api_key = settings.PAYSTACK_SECRET_KEY


def create_property_flutterwave_payment_link(
    property_instance: Property, user: AbstractUser
) -> str:
    """
    Create a Flutterwave payment link for a property checkout session.
    """
    url = "https://api.flutterwave.com/v3/payments"
    checkout = PropertyCheckout.objects.create(
        property=property_instance,
        user=user,
        payment_gateway="flutterwave",
        status="initiated",
    )
    payload = {
        "amount": str(int(property_instance.price)),
        "tx_ref": str(checkout.id),
        "currency": "NGN",
        "redirect_url": settings.FLUTTERWAVE_REDIRECT_URL,
        "customer": {"email": user.email, "name": f"{user.get_full_name()}"},
        "customizations": {
            "title": "Duke Real Estate",
            "description": f"Payment for {property_instance.subtitle()}",
            "logo": "https://de-duke.com/static/logo.png",
        },
        "configuration": {"session_duration": 30},
        "max_retry_attempt": 5,
        "payment_options": "card, opay, banktransfer, account, applepay, googlepay, enaira",
        # "link_expiration": "2024-02-14T12:20:00",
        "meta": {
            "property_id": str(property_instance.id),
            "user_id": str(user.id),
            # "valid_until": checkout.created_at.isoformat()
        },
    }
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + settings.FLUTTERWAVE_SECRET_KEY,
        "Content-Type": "application/json",
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        if response_data.get("status") == "success":
            payment_link = response_data["data"]["link"]
            return payment_link
        else:
            raise Exception(f"Flutterwave API error: {response_data.get('message')}")
    else:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")


# def create_property_paystack_payment_link(property_instance: Property, user: AbstractUser) -> str:
#     """
#     Create a Paystack payment link for a property checkout session.
#     """
#     checkout = PropertyCheckout.objects.create(
#         property=property_instance,
#         user=user,
#         payment_gateway='paystack',
#         status='initiated'
#     )
#     transaction = paystack.Transaction.initialize(
#         amount=property_instance.unit_amount,
#         currency=checkout.currency,
#         email=user.email,
#         reference=checkout.id,
#         metadata={
#             "property_id": str(property_instance.id),
#             "user_id": str(user.id),
#             # "valid_until": checkout.created_at.isoformat()
#         }
#     )
#     return transaction.data["access_code"]


def create_property_chat_invoice_paystack_payment_link(
    property_chat_invoice: PropertyChatInvoice,
) -> str:
    """
    Create a Paystack payment access code for a property chat invoice.
    """
    metadata = {
        "invoice_id": str(property_chat_invoice.id),
        "property_id": str(property_chat_invoice.property_chat.property.id),
        "user_id": str(property_chat_invoice.property_chat.client.id),
        "possession_period_start_date": property_chat_invoice.possession_period_start_date.isoformat(),
    }
    if property_chat_invoice.possession_period_end_date:
        metadata["possession_period_end_date"] = (
            property_chat_invoice.possession_period_end_date.isoformat()
        )
    transaction = paystack.Transaction.initialize(
        amount=property_chat_invoice.unit_amount,
        currency=property_chat_invoice.currency,
        email=property_chat_invoice.property_chat.client.email,
        metadata=metadata,
    )
    print("Transaction: ", transaction, transaction.data)
    return transaction.data["authorization_url"]
