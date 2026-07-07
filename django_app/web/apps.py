from django.apps import AppConfig


class WebConfig(AppConfig):
    """Application configuration for the image analysis workflow."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "web"