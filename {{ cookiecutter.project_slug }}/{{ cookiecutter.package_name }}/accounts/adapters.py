from typing import TYPE_CHECKING

from allauth.account.adapter import DefaultAccountAdapter
from constance import config

if TYPE_CHECKING:
    from django.http import HttpRequest

    from .models import User


class AccountAdapter(DefaultAccountAdapter):
    """A django-allauth adapter for customizing authn flows."""

    def is_open_for_signup(self, request: "HttpRequest") -> bool:
        """Return True if users can open accounts."""
        return config.ACCOUNTS_REGISTRATION_OPEN
