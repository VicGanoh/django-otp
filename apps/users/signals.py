import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.users.models import OTPVerification, User


logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def create_otp_verification(sender, instance, created, **kwargs):
    if created:
       otp_verification = OTPVerification.objects.create(user=instance)
       otp_verification.generate_otp()
       otp_code = otp_verification.get_otp()

       logger.info("User OTP successfully created with code: %s", otp_code)
       logger.info("OTP verfied: %r", otp_verification.verify_otp(otp_code))
