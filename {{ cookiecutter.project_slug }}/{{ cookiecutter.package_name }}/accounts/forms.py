from allauth.account.forms import SignupForm as BaseSignupForm
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Invisible


class SignupForm(BaseSignupForm):
    """Registration form for creating new accounts.

    Extends the django-allauth signup form to add support for reCAPTCHA.
    """

    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)
