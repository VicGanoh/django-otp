from django.apps import AppConfig
import logging


class DjangoOtpConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.users"

    def ready(self) -> None:
        try:
            import apps.users.signals
        except ImportError:
            logging.exception("Failed to import signals.")