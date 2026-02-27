from django.contrib import admin

from .models import PropertyChatInvoice


@admin.register(PropertyChatInvoice)
class PropertyChatInvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "payment_gateway",
        "currency",
        "amount",
        "is_sealed",
        "status",
    )
    list_filter = ("payment_gateway", "currency", "status", "is_sealed")
    ordering = ("-created_at",)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
