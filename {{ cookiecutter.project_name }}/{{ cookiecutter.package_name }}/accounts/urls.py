from django.urls import re_path

from {{ cookiecutter.package_name }}.accounts import views

app_name = "accounts"

urlpatterns = [
    re_path(
        r"^two_factor/setup/?$",
        views.TwoFactorSetup.as_view(),
        name="two-factor-setup",
    ),
]
