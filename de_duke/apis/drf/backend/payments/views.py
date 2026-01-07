from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action, authentication_classes, permission_classes
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import permissions

from .models import PropertyCheckout
from .serializers import PropertyCheckoutResponseSerializer, PropertyCheckoutRequestSerializer
from .utility import (create_property_flutterwave_payment_link,
                      create_property_paystack_payment_link)
from properties.models import Property


class FlutterwavePaymentViewSet(viewsets.ViewSet):

    # Create property checkout session
    @extend_schema(
        request=PropertyCheckoutRequestSerializer,
        responses={
            status.HTTP_200_OK: PropertyCheckoutResponseSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad Request"
        },
        summary="Create Property Checkout Session",
        description="Create a checkout session for a property using Flutterwave."
    )
    @action(detail=False, methods=['post'], url_path='create-property-checkout-session')
    def create_property_checkout_session(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = PropertyCheckoutRequestSerializer(data=request.data)
        if serializer.is_valid():
            property_id = serializer.validated_data['property_id']
            try:
                property_instance = Property.objects.get(id=property_id)
            except Property.DoesNotExist:
                return Response({"error": "Property not found."}, status=status.HTTP_404_NOT_FOUND)

            payment_link = create_property_flutterwave_payment_link(
                property_instance, request.user)
            response_serializer = PropertyCheckoutResponseSerializer(
                {"payment_link": payment_link})
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaystackPaymentViewSet(viewsets.ViewSet):
    @extend_schema(
        request=PropertyCheckoutRequestSerializer,
        responses={
            status.HTTP_200_OK: PropertyCheckoutResponseSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad Request"
        },
        summary="Initialize Property Checkout",
        description="Initialize a checkout for a property using Paystack."
    )
    @permission_classes([permissions.IsAuthenticated])
    @action(detail=False, methods=['post'], url_path='initialize')
    def initialize(self, request):
        serializer = PropertyCheckoutRequestSerializer(data=request.data)
        if serializer.is_valid():
            property_id = serializer.validated_data['property_id']
            try:
                property_instance = Property.objects.get(id=property_id)
            except Property.DoesNotExist:
                return Response({"error": "Property not found."}, status=status.HTTP_404_NOT_FOUND)

            access_code = create_property_paystack_payment_link(
                property_instance, request.user)
            response_serializer = PropertyCheckoutResponseSerializer(
                {"access_code": access_code})
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
