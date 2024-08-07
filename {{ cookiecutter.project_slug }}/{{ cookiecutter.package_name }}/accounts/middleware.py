from collections.abc import Callable
from typing import TYPE_CHECKING, cast

from allauth.mfa.utils import is_mfa_enabled
from django.conf import settings
from django.shortcuts import redirect
from django.urls import resolve, reverse
from django.utils import timezone

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse

    from .models import User


class Enforce2FAMiddleware:
    """A middleware for enforcing the use of 2-factor authentication."""

    MFA_SETUP_URL_NAME = "mfa_activate_totp"
    EXEMPT_URL_NAMES = (
        MFA_SETUP_URL_NAME,
        "mfa_reauthenticate",
        "account_reauthenticate",
        "mfa_reauthenticate_webauthn",
    )

    def __init__(self, get_response: Callable[["HttpRequest"], "HttpResponse"]) -> None:
        self.get_response = get_response

    def __call__(self, request: "HttpRequest") -> "HttpResponse":
        """Return True if the user is required to use 2-factor auth."""
        # Skip this middleware if MFA is disabled.
        if not settings.MFA_ENABLED:
            return self.get_response(request)

        # Skip this middleware for users that are not logged in
        if not request.user.is_authenticated:
            return self.get_response(request)

        # Skip the middleware for exempted URLs (mostly to prevent infinite
        # redirects).
        destination_url_name = resolve(request.path).url_name
        if destination_url_name in self.EXEMPT_URL_NAMES:
            return self.get_response(request)

        # Skip the middleware for users that already have 2FA enabled.
        user = cast("User", request.user)
        if is_mfa_enabled(user) or not user.require_2fa:
            return self.get_response(request)

        mfa_setup_url = f"{reverse(self.MFA_SETUP_URL_NAME)}?next={request.path}"

        return redirect(mfa_setup_url)


class TimeZoneMiddleware:
    """A middleware to set the active time zone based on user settings."""

    def __init__(self, get_response: Callable[["HttpRequest"], "HttpResponse"]) -> None:
        self.get_response = get_response

    def __call__(self, request: "HttpRequest") -> "HttpResponse":
        """Activate the appropriate time zone for the user.

        If the user is anonymous, deactivate the timezone and use the default.
        """
        if request.user.is_authenticated:
            timezone.activate(cast("User", request.user).time_zone)
        else:
            timezone.deactivate()
        return self.get_response(request)
