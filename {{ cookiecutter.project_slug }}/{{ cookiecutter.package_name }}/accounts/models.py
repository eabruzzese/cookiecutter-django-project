from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from timezone_field import TimeZoneField


class User(AbstractUser):
    """A user account."""

    email = models.EmailField(
        verbose_name=_("email address"),
        max_length=255,
        unique=True,
    )
    time_zone = TimeZoneField(default="America/New_York")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username",)

    @property
    def require_2fa(self) -> bool:
        """Return True if the user should be required to authenticate with 2FA."""
        if not settings.ACCOUNTS_STAFF_REQUIRE_2FA:
            return False
        return self.is_staff or self.is_superuser
