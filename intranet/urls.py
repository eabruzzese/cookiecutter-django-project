"""intranet URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/

Examples:
    Function views
        1. Add an import:  from my_app import views
        2. Add a URL to urlpatterns:  path('', views.home, name='home')
    Class-based views
        1. Add an import:  from other_app.views import Home
        2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
    Including another URLconf
        1. Import the include() function: from django.urls import include, path
        2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import include, path, re_path

# Force administrative users to log in via the django-allauth flows to take
# advantage of security features like ReCAPTCHA and lockouts.
admin.site.login = staff_member_required(admin.site.login, login_url=settings.LOGIN_URL)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("intranet.accounts.urls", namespace="accounts")),
    # NOTE: The django-allauth package does not support namespacing, and so we
    #       must include them in the root URL config.
    path("accounts/", include("allauth_2fa.urls")),
    path("accounts/", include("allauth.urls")),
    re_path(r"healthcheck/?", include("health_check.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
]
