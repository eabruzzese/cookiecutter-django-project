from typing import Any

from allauth.account.forms import SignupForm as BaseSignupForm
from allauth.mfa.totp.forms import ActivateTOTPForm as BaseActivateTOTPForm
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Invisible


class SignupForm(BaseSignupForm):
    """Registration form for creating new accounts.

    Extends the django-allauth signup form to add support for reCAPTCHA.
    """

    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)


class ActivateTOTPForm(BaseActivateTOTPForm):
    """A form for activating a TOTP authenticator."""

    email_verified: bool

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        # Don't require email verification for superusers.
        self.email_verified = self.user.is_superuser or self.email_verified
