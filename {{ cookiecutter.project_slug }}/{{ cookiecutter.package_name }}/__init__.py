# Ensure that the app is always imported when Django starts so that shared_task
# will use it.

import django_stubs_ext

from .celery import app as celery_app

django_stubs_ext.monkeypatch()

__all__ = ("celery_app",)
