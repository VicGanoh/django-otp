from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
import uuid
import pyotp
from datetime import timedelta
from django.utils import timezone

class CustomUserManager(UserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Please provide a phone number")

        user = self.model(
            phone_number=phone_number,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        user = self.create_user(phone_number, password=password, **extra_fields)

        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    id = models.UUIDField(_("ID"), primary_key=True, default=uuid.uuid4(), unique=True, editable=False)
    first_name = models.CharField(_("First name"), max_length=150, blank=True)
    last_name = models.CharField(_("Last name"), max_length=150, blank=True)
    phone_number = PhoneNumberField(_("Phone number"), unique=True)
    username = None
    
    objects = CustomUserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["first_name", "last_name",]

    class Meta:
        db_table = "users"
        verbose_name = _("user")
        verbose_name_plural = _("users")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.full_name}"


class OTPVerification(models.Model):
    id = models.UUIDField(_("ID"), primary_key=True, default=uuid.uuid4(), unique=True, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="otp_verification",
    )
    otp_code = models.CharField(_("OTP code"), max_length=6, blank=True, default="")
    secret_key = models.CharField(max_length=50, unique=True, blank=True)
    verified = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("OTP Verification")
        verbose_name_plural = _("OTP Verifications")
    
    def __str__(self):
        return str(self.user)
    
    def generate_secret_key(self):
        """Generate a secret key"""
        return pyotp.random_base32()

    @property
    def is_random_secret_key_verified(self):
        return self.secret_key == self.generate_secret_key()
    
    def generate_otp(self):
        if self.is_random_secret_key_verified:
            return pyotp.TOTP(self.secret_key)
    
    def get_otp(self):
        return self.generate_otp().now()
    
    def has_expired(self):
        """
        Check if OTP is expired
        """
        return self.created_at + timedelta(seconds=self.generate_otp().interval) < timezone.now()
    
    @classmethod
    def create_otp_verification(cls, user: User):
        """
        Create a new OTP verification for the given user.
        """
        return cls.objects.create(user=user)

    def save(self, *args, **kwargs):
        if not self.secret_key:
           self.secret_key = self.generate_secret_key
        super(OTPVerification, self).save(*args, **kwargs)