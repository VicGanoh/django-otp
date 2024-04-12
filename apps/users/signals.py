# import logging

# from django.contrib.auth import get_user_model
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from apps.users.models import OTPVerification

# User = get_user_model()

# logger = logging.getLogger(__name__)

# @receiver(post_save, sender=User)
# def create_otp_verification(sender, instance, created, **kwargs):
#     if created:
#        otp = OTPVerification.create_otp_verification(instance)

#        logger.info("User OTP created with code: %s", otp.generate_otp())