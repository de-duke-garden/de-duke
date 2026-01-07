from rest_framework import serializers


class PropertyCheckoutRequestSerializer(serializers.Serializer):
    property_id = serializers.CharField(max_length=255)


class CheckoutResponseSerializer(serializers.Serializer):
    access_code = serializers.CharField(required=False)
    payment_link = serializers.URLField(required=False)


class PropertyCheckoutResponseSerializer(CheckoutResponseSerializer):
    pass
