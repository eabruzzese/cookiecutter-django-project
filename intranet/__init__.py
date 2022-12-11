# Ensure that the app is always imported when Django starts so that shared_task
# will use it.

from .celery import app as celery_app  # noqa

__all__ = ("celery_app",)
