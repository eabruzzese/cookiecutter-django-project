from django.conf import settings
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import include, path, re_path
from django.views.generic import RedirectView

# Force administrative users to log in via the django-allauth flows to take
# advantage of security features like ReCAPTCHA and lockouts.
admin.site.login = staff_member_required(admin.site.login, login_url=settings.LOGIN_URL)

urlpatterns = [
    path("", RedirectView.as_view(url=settings.LOGIN_URL)),
    path("admin/", admin.site.urls),
    path("accounts/", include("{{ cookiecutter.package_name }}.accounts.urls", namespace="accounts")),
    # NOTE: The django-allauth package does not support namespacing, and so we
    #       must include them in the root URL config.
    path("accounts/", include("allauth_2fa.urls")),
    path("accounts/", include("allauth.urls")),
    re_path(r"healthcheck/?", include("health_check.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
]
