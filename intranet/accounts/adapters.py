from typing import TYPE_CHECKING

from allauth_2fa.adapter import OTPAdapter
from constance import config

if TYPE_CHECKING:
    from django.http import HttpRequest

    from .models import User


class AccountAdapter(OTPAdapter):
    """A django-allauth adapter for customizing authn flows."""

    def is_open_for_signup(self, request: "HttpRequest") -> bool:
        """Return True if users can open accounts."""
        return config.ACCOUNTS_REGISTRATION_OPEN

    def login(self, request: "HttpRequest", user: "User") -> None:
        """Authenticate the given user."""
        # Patch an issue where some of the django-allauth views do not have a
        # redirect_field_name (it's always 'next').
        view = request.resolver_match.func.view_class
        view.redirect_field_name = getattr(view, "redirect_field_name", "next")
        return super().login(request, user)
