from rest_framework import serializers
from .models import PropertyChatInvoice


class PropertyCheckoutRequestSerializer(serializers.Serializer):
    property_id = serializers.CharField(max_length=255)


class CheckoutResponseSerializer(serializers.Serializer):
    access_code = serializers.CharField(required=False)
    payment_link = serializers.URLField(required=False)


class PropertyCheckoutResponseSerializer(CheckoutResponseSerializer):
    pass


class PropertyChatInvoiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyChatInvoice
        fields = ["property_chat", "possession_period_start_date"]


class PropertyChatInvoiceEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyChatInvoice
        fields = ["id", "possession_period_start_date"]
        read_only_fields = ["id"]


class PropertyChatInvoiceSealSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyChatInvoice
        fields = ["id", "is_sealed"]
        read_only_fields = ["id"]


class PropertyChatInvoiceSerializer(serializers.ModelSerializer):
    amount = serializers.CharField()

    class Meta:
        model = PropertyChatInvoice
        fields = "__all__"
