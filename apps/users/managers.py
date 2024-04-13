from django.contrib.auth.models import UserManager
from django.contrib.auth.hashers import make_password

class CustomUserManager(UserManager):
    """Custom manager for the User model."""

    def _create_user(self, phone_number, password=None, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not phone_number:
            msg = "The given phone number must be set"
            raise ValueError(msg)
        user = self.model(phone_number=phone_number, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            msg = "Superuser must have is_staff=True."
            raise ValueError(msg)
        if extra_fields.get("is_superuser") is not True:
            msg = "Superuser must have is_superuser=True."
            raise ValueError(msg)

        return self._create_user(phone_number, password, **extra_fields)