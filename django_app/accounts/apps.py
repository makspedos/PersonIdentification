from django.apps import AppConfig


class AccountConfig(AppConfig):
    """Application configuration for account views, forms, and templates."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"