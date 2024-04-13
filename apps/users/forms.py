from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User
        fields = ("phone_number", "first_name", "last_name", "is_active", "is_staff", "is_superuser")


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ("phone_number", "first_name", "last_name", "is_active", "is_staff", "is_superuser")
        error_messages = {
            "phone_number": {"unique": _("This phone_number has already been taken.")},
        }