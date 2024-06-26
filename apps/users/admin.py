from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from apps.users.models import User, OTPVerification
from django.utils.translation import gettext_lazy as _


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
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
                "fields": (
                    "first_name",
                    "last_name",
                    "phone_number",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    list_display = ("id", "phone_number", "first_name", "last_name", "is_staff",)
    ordering = ("phone_number",)
    search_fields = ("first_name", "last_name", )


@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "secret_key", "verified", "created_at")

    def user(self, obj):
        return obj.user.full_name