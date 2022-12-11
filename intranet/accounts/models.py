from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """An intranet user."""

    email = models.EmailField(
        verbose_name=_("email address"),
        max_length=255,
        unique=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username",)
