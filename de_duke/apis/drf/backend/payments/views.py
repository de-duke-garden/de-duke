from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action, authentication_classes, permission_classes
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import permissions
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.request import Request
import hmac
import hashlib
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import PropertyChatInvoice
from .serializers import (
    PropertyCheckoutResponseSerializer,
    PropertyCheckoutRequestSerializer,
    PropertyChatInvoiceSerializer,
)
from .utility import (
    create_property_flutterwave_payment_link,
    # create_property_paystack_payment_link,
)
from properties.models import Property
from utilities.payload import Payload
from utilities.chat_helper import get_recipients_by_chat_id


class FlutterwavePaymentViewSet(viewsets.ViewSet):
    # Create property checkout session
    @extend_schema(
        request=PropertyCheckoutRequestSerializer,
        responses={
            status.HTTP_200_OK: PropertyCheckoutResponseSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad Request",
        },
        summary="Create Property Checkout Session",
        description="Create a checkout session for a property using Flutterwave.",
    )
    @action(detail=False, methods=["post"], url_path="create-property-checkout-session")
    def create_property_checkout_session(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"error": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        serializer = PropertyCheckoutRequestSerializer(data=request.data)
        if serializer.is_valid():
            property_id = serializer.validated_data["property_id"]
            try:
                property_instance = Property.objects.get(id=property_id)
            except Property.DoesNotExist:
                return Response(
                    {"error": "Property not found."}, status=status.HTTP_404_NOT_FOUND
                )

            payment_link = create_property_flutterwave_payment_link(
                property_instance, request.user
            )
            response_serializer = PropertyCheckoutResponseSerializer(
                {"payment_link": payment_link}
            )
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaystackPaymentViewSet(viewsets.ViewSet):
    # @extend_schema(
    #     request=PropertyCheckoutRequestSerializer,
    #     responses={
    #         status.HTTP_200_OK: PropertyCheckoutResponseSerializer,
    #         status.HTTP_400_BAD_REQUEST: "Bad Request",
    #     },
    #     summary="Initialize Property Checkout",
    #     description="Initialize a checkout for a property using Paystack.",
    # )
    # @permission_classes([permissions.IsAuthenticated])
    # @action(detail=False, methods=["post"], url_path="initialize")
    # def initialize(self, request):
    #     serializer = PropertyCheckoutRequestSerializer(data=request.data)
    #     if serializer.is_valid():
    #         property_id = serializer.validated_data["property_id"]
    #         try:
    #             property_instance = Property.objects.get(id=property_id)
    #         except Property.DoesNotExist:
    #             return Response(
    #                 {"error": "Property not found."}, status=status.HTTP_404_NOT_FOUND
    #             )

    #         access_code = create_property_paystack_payment_link(
    #             property_instance, request.user
    #         )
    #         response_serializer = PropertyCheckoutResponseSerializer(
    #             {"access_code": access_code}
    #         )
    #         return Response(response_serializer.data, status=status.HTTP_200_OK)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={
            status.HTTP_200_OK: "OK",
            status.HTTP_400_BAD_REQUEST: "Bad Request",
        },
        summary="Paystack Webhook",
        description="Paystack Webhook.",
    )
    @permission_classes([permissions.AllowAny])
    @action(detail=False, methods=["post"], url_path="webhook")
    def webhook(self, request):
        # Get raw request body (important for signature verification)
        payload = request.body
        # Generate HMAC SHA512 hash
        secret = settings.PAYSTACK_SECRET_KEY
        computed_hash = hmac.new(secret.encode(), payload, hashlib.sha512).hexdigest()
        # Get signature from headers
        signature = request.headers.get("x-paystack-signature")
        # Verify signature
        if hmac.compare_digest(computed_hash, signature):
            # Signature is valid, process the webhook
            # {
            #     "event": "charge.success",
            #     "data": {
            #         "id": 302961,
            #         "domain": "live",
            #         "status": "success",
            #         "reference": "qTPrJoy9Bx",
            #         "amount": 10000,
            #         "message": null,
            #         "gateway_response": "Approved by Financial Institution",
            #         "paid_at": "2016-09-30T21:10:19.000Z",
            #         "created_at": "2016-09-30T21:09:56.000Z",
            #         "channel": "card",
            #         "currency": "NGN",
            #         "ip_address": "41.242.49.37",
            #         "metadata": 0,
            #         "log": {
            #         "time_spent": 16,
            #         "attempts": 1,
            #         "authentication": "pin",
            #         "errors": 0,
            #         "success": false,
            #         "mobile": false,
            #         "input": [],
            #         "channel": null,
            #         "history": [
            #             {
            #             "type": "input",
            #             "message": "Filled these fields: card number, card expiry, card cvv",
            #             "time": 15
            #             },
            #             {
            #             "type": "action",
            #             "message": "Attempted to pay",
            #             "time": 15
            #             },
            #             {
            #             "type": "auth",
            #             "message": "Authentication Required: pin",
            #             "time": 16
            #             }
            #         ]
            #         },
            #         "fees": null,
            #         "customer": {
            #         "id": 68324,
            #         "first_name": "BoJack",
            #         "last_name": "Horseman",
            #         "email": "bojack@horseman.com",
            #         "customer_code": "CUS_qo38as2hpsgk2r0",
            #         "phone": null,
            #         "metadata": null,
            #         "risk_action": "default"
            #         },
            #         "authorization": {
            #         "authorization_code": "AUTH_f5rnfq9p",
            #         "bin": "539999",
            #         "last4": "8877",
            #         "exp_month": "08",
            #         "exp_year": "2020",
            #         "card_type": "mastercard DEBIT",
            #         "bank": "Guaranty Trust Bank",
            #         "country_code": "NG",
            #         "brand": "mastercard",
            #         "account_name": "BoJack Horseman"
            #         },
            #         "plan": {}
            #     }
            # }
            event = payload.get("event")
            data = payload.get("data")
            if event == "charge.success":
                invoice = PropertyChatInvoice.objects.get(
                    id=data["metadata"]["invoice_id"]
                )
                invoice.status = "successful"
                invoice.save()
                invoice.property_chat.allow_payment = False
                invoice.property_chat.save()
                channel_layer = get_channel_layer()
                ws_payload = Payload(
                    action="payment_success",
                    data={
                        "invoice_id": invoice.id,
                        "property_chat_id": invoice.property_chat.id,
                        "status": invoice.status,
                    },
                )
                recipients = get_recipients_by_chat_id(invoice.property_chat.id)
                for recipient in recipients:
                    async_to_sync(channel_layer.group_send)(
                        recipient,
                        {
                            "type": "group.payload.handler",
                            "payload": ws_payload.to_json(),
                        },
                    )
        else:
            # Signature is invalid, reject the request
            print("Invalid signature.")
            return Response(
                {"error": "Invalid signature."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class PaymentsViewSet(viewsets.ViewSet):
    @action(
        detail=False,
        methods=["get"],
        renderer_classes=[TemplateHTMLRenderer],
        url_path="redirect",
    )
    def redirect(self, request: Request):
        query_params = request.query_params
        print("Query Params: ", query_params)
        template_name = None
        if query_params.get("status") == "failed":
            template_name = "payments/failed.html"
        else:
            template_name = "payments/success.html"
        return Response(
            {"message": "Redirect"},
            status=status.HTTP_200_OK,
            template_name=template_name,
        )

    @extend_schema(
        responses={
            status.HTTP_200_OK: "OK",
            status.HTTP_400_BAD_REQUEST: "Bad Request",
        },
        summary="Paystack Webhook",
        description="Paystack Webhook.",
    )
    @permission_classes([permissions.AllowAny])
    @action(detail=False, methods=["post"], url_path="paystack/webhook")
    def paystack_webhook(self, request):
        # Get raw request body (important for signature verification)
        payload = request.body
        # Generate HMAC SHA512 hash
        secret = settings.PAYSTACK_SECRET_KEY
        computed_hash = hmac.new(secret.encode(), payload, hashlib.sha512).hexdigest()
        # Get signature from headers
        signature = request.headers.get("x-paystack-signature")
        # Verify signature
        if hmac.compare_digest(computed_hash, signature):
            # Signature is valid, process the webhook
            # {
            #     "event": "charge.success",
            #     "data": {
            #         "id": 302961,
            #         "domain": "live",
            #         "status": "success",
            #         "reference": "qTPrJoy9Bx",
            #         "amount": 10000,
            #         "message": null,
            #         "gateway_response": "Approved by Financial Institution",
            #         "paid_at": "2016-09-30T21:10:19.000Z",
            #         "created_at": "2016-09-30T21:09:56.000Z",
            #         "channel": "card",
            #         "currency": "NGN",
            #         "ip_address": "41.242.49.37",
            #         "metadata": 0,
            #         "log": {
            #         "time_spent": 16,
            #         "attempts": 1,
            #         "authentication": "pin",
            #         "errors": 0,
            #         "success": false,
            #         "mobile": false,
            #         "input": [],
            #         "channel": null,
            #         "history": [
            #             {
            #             "type": "input",
            #             "message": "Filled these fields: card number, card expiry, card cvv",
            #             "time": 15
            #             },
            #             {
            #             "type": "action",
            #             "message": "Attempted to pay",
            #             "time": 15
            #             },
            #             {
            #             "type": "auth",
            #             "message": "Authentication Required: pin",
            #             "time": 16
            #             }
            #         ]
            #         },
            #         "fees": null,
            #         "customer": {
            #         "id": 68324,
            #         "first_name": "BoJack",
            #         "last_name": "Horseman",
            #         "email": "bojack@horseman.com",
            #         "customer_code": "CUS_qo38as2hpsgk2r0",
            #         "phone": null,
            #         "metadata": null,
            #         "risk_action": "default"
            #         },
            #         "authorization": {
            #         "authorization_code": "AUTH_f5rnfq9p",
            #         "bin": "539999",
            #         "last4": "8877",
            #         "exp_month": "08",
            #         "exp_year": "2020",
            #         "card_type": "mastercard DEBIT",
            #         "bank": "Guaranty Trust Bank",
            #         "country_code": "NG",
            #         "brand": "mastercard",
            #         "account_name": "BoJack Horseman"
            #         },
            #         "plan": {}
            #     }
            # }
            event = payload.get("event")
            data = payload.get("data")
            if event == "charge.success":
                invoice = PropertyChatInvoice.objects.get(
                    id=data["metadata"]["invoice_id"]
                )
                invoice.status = "successful"
                invoice.save()
                invoice.property_chat.allow_payment = False
                invoice.property_chat.save()
                channel_layer = get_channel_layer()
                ws_payload = Payload(
                    action="payment_success",
                    data={
                        "invoice": PropertyChatInvoiceSerializer(instance=invoice).data,
                        "status": invoice.status,
                    },
                )
                recipients = get_recipients_by_chat_id(invoice.property_chat.id)
                for recipient in recipients:
                    async_to_sync(channel_layer.group_send)(
                        recipient,
                        {
                            "type": "group.payload.handler",
                            "payload": ws_payload.to_json(),
                        },
                    )
        else:
            # Signature is invalid, reject the request
            print("Invalid signature.")
            return Response(
                {"error": "Invalid signature."},
                status=status.HTTP_400_BAD_REQUEST,
            )
