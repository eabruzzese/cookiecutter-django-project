from django.conf import settings
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from health_check.views import HealthCheckView
from redis.asyncio import Redis as RedisClient

# Force administrative users to log in via the django-allauth flows to take
# advantage of security features like ReCAPTCHA and lockouts.
admin.site.login = staff_member_required(admin.site.login, login_url=settings.LOGIN_URL)

urlpatterns = [
    path("", RedirectView.as_view(url=settings.LOGIN_URL)),
    path("admin/", admin.site.urls),
    # NOTE: The django-allauth package does not support namespacing, and so we
    #       must include them in the root URL config.
    path("accounts/", include("allauth.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    re_path(
        r"healthcheck/?",
        HealthCheckView.as_view(
            checks=[  # optional, default is all but 3rd party checks
                "health_check.Cache",
                "health_check.DNS",
                "health_check.Database",
                "health_check.Mail",
                "health_check.Storage",
                # 3rd party checks
                "health_check.contrib.psutil.Disk",
                "health_check.contrib.psutil.Memory",
                "health_check.contrib.celery.Ping",
                (
                    "health_check.contrib.redis.Redis",
                    {"client_factory": lambda: RedisClient.from_url(settings.CACHE_URL)},
                ),
            ],
        ),
    ),
]
