from base64 import b32encode
from typing import Any

from allauth_2fa.views import TwoFactorSetup as BaseTwoFactorSetup


class TwoFactorSetup(BaseTwoFactorSetup):
    """A view extending TwoFactorSetup to expose the secret key to the view.

    This allows the user to enter the code manually, which is useful for users who are not able to
    scan the QR code.
    """

    def get_secret_utf8(self) -> str:
        """Return the secret key as utf-8."""
        return b32encode(self.device.bin_key).decode()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Return the render context for the 2FA setup page."""
        return {**super().get_context_data(**kwargs), "secret": self.get_secret_utf8()}
