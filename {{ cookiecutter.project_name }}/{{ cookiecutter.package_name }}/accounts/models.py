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
