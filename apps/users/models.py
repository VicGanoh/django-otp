from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
import uuid
import pyotp
from datetime import timedelta
from django.utils import timezone
from .managers import CustomUserManager


class User(AbstractUser):
    id = models.UUIDField(_("ID"), primary_key=True, default=uuid.uuid4(), unique=True, editable=False)
    first_name = models.CharField(_("First name"), max_length=150)
    last_name = models.CharField(_("Last name"), max_length=150)
    phone_number = PhoneNumberField(_("Phone number"), unique=True)
    username = None

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["first_name", "last_name",]
    
    objects = CustomUserManager()

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
        related_name="otp_verifications",
    )
    secret_key = models.CharField(max_length=50, unique=True, blank=True)
    verified = models.BooleanField(default=False)
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
    
    def generate_otp(self):
        if self.secret_key:
            return pyotp.TOTP(self.secret_key, interval=180)
    
    def get_otp(self):
        """
        Get the current otp
        """
        return self.generate_otp().now()
    
    def is_verified(self, code):
        """Verify the provided code against the generated code."""
        is_verified = self.generate_otp().verify(code)
        self.verified = is_verified
        self.save()
        return is_verified
    
    def has_expired(self) -> bool:
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
           self.secret_key = self.generate_secret_key()
        super(OTPVerification, self).save(*args, **kwargs)