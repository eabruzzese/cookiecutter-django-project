from django.apps import AppConfig


class TenantsConfig(AppConfig):
    """An application config for the tenants app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "{{ cookiecutter.package_name }}.tenants"
