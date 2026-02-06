import nested_admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from utilities.mixins import ImageUploaderWidgetAdminMixin

from .models import OTPRequest, User, PhoneNumber
from .models import (
    HostAccountAgent,
    HostAccountArchitect,
    HostAccountCompany,
    HostAccountLawyer,
    HostAccountOwner,
    HostAccountSurveyor,
)


admin.site.site_header = "De-Duke Garden Care"
admin.site.site_title = "De-Duke Garden Care administration"
admin.site.index_title = "Welcome to De-Duke Admin Dashboard"


class PhoneNumberInline(nested_admin.NestedTabularInline):
    model = PhoneNumber
    extra = 0
    max_num = 1


# class HostAccountInline(nested_admin.NestedStackedInline):
#     model = HostAccount
#     extra = 0
#     max_num = 1


@admin.register(User)
class UserAdmin(
    ImageUploaderWidgetAdminMixin, BaseUserAdmin, nested_admin.NestedModelAdmin
):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "email_verified",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "first_name", "password1", "password2"),
            },
        ),
    )
    list_display = ("email", "first_name", "last_name", "is_staff")
    search_fields = ("first_name", "last_name", "email")
    ordering = ("email",)
    inlines = [
        PhoneNumberInline,
        # HostAccountInline
    ]


# @admin.register(OTPRequest)
# class OTPRequestAdmin(nested_admin.NestedModelAdmin):
#     list_display = ("ref", "otp", "is_verified", "has_expired", "created_at")
#     search_fields = ("ref",)
#     ordering = ("-created_at",)
#     list_filter = ("created_at",)


class HostAccountAdminMixin:
    list_display = ("user", "status", "created_at")
    search_fields = ("user__email", "user__first_name", "user__last_name")
    list_filter = ("status",)
    ordering = ("-created_at",)

    def get_exclude(self, request, obj=None):
        exclude = ["type"]
        # if obj is None:
        #     exclude.extend(['address', 'listed_by'])
        return exclude

    def has_add_permission(self, request, obj=None):
        # Prevent adding HostAccount from admin
        return False

    def has_delete_permission(self, request, obj=None):
        # Prevent deleting HostAccount from admin
        return False


@admin.register(HostAccountAgent)
class HostAccountAgentAdmin(
    ImageUploaderWidgetAdminMixin, HostAccountAdminMixin, nested_admin.NestedModelAdmin
):
    pass


@admin.register(HostAccountArchitect)
class HostAccountArchitectAdmin(
    ImageUploaderWidgetAdminMixin, HostAccountAdminMixin, nested_admin.NestedModelAdmin
):
    pass


@admin.register(HostAccountCompany)
class HostAccountCompanyAdmin(
    ImageUploaderWidgetAdminMixin, HostAccountAdminMixin, nested_admin.NestedModelAdmin
):
    pass


@admin.register(HostAccountLawyer)
class HostAccountLawyerAdmin(
    ImageUploaderWidgetAdminMixin, HostAccountAdminMixin, nested_admin.NestedModelAdmin
):
    pass


@admin.register(HostAccountOwner)
class HostAccountOwnerAdmin(
    ImageUploaderWidgetAdminMixin, HostAccountAdminMixin, nested_admin.NestedModelAdmin
):
    pass


@admin.register(HostAccountSurveyor)
class HostAccountSurveyorAdmin(
    ImageUploaderWidgetAdminMixin, HostAccountAdminMixin, nested_admin.NestedModelAdmin
):
    pass
