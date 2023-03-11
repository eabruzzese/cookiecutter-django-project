from allauth.account.forms import SignupForm as BaseSignupForm
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible


class SignupForm(BaseSignupForm):
    """Registration form for creating new accounts.

    Extends the django-allauth signup form to add support for reCAPTCHA.
    """

    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)
