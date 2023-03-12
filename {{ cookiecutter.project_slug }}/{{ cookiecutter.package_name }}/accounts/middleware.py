from collections.abc import Callable
from typing import TYPE_CHECKING, cast

from allauth_2fa.middleware import BaseRequire2FAMiddleware
from django.utils import timezone

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse

    from .models import User


class Enforce2FAMiddleware(BaseRequire2FAMiddleware):
    """A middleware for enforcing the use of 2-factor authentication."""

    def require_2fa(self, request: "HttpRequest") -> bool:
        """Return True if the user is required to use 2-factor auth."""
        user = cast("User", request.user)
        return user.require_2fa


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
