from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
import uuid
import pyotp
from datetime import timedelta
from django.utils import timezone
from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(_("ID"), primary_key=True, default=uuid.uuid4(), unique=True, editable=False)
    first_name = models.CharField(_("First name"), max_length=150, blank=True)
    last_name = models.CharField(_("Last name"), max_length=150, blank=True)
    phone_number = PhoneNumberField(_("Phone number"), unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
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
    
    def verify_otp(self, otp):
        """
        Verify the provided OTP against the generated OTP.
        """
        if self.generate_otp().verify(otp):
            self.verified = True
        else:
            self.verified = False
        self.save()
    
    def has_expired(self) -> bool:
        """
        Check if OTP is expired
        """
        return self.created_at + timedelta(seconds=self.generate_otp().interval) < timezone.now()
    
    # @classmethod
    # def create_otp_verification(cls, user: User):
    #     """
    #     Create a new OTP verification for the given user.
    #     """
    #     return cls.objects.create(user=user)

    def save(self, *args, **kwargs):
        if not self.secret_key:
           self.secret_key = self.generate_secret_key()
        super(OTPVerification, self).save(*args, **kwargs)