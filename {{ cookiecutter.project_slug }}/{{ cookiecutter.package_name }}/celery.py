import os
from typing import TYPE_CHECKING

from celery import Celery

if TYPE_CHECKING:
    from celery import Task

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{{ cookiecutter.package_name }}.settings")

app = Celery("{{ cookiecutter.package_name }}")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
#
# - namespace="CELERY" means all celery-related configuration keys
#   should have a `CELERY_` prefix.
#
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(task: "Task") -> None:
    """A task for debugging requests to the celery workers.

    We define it here -- as close to the initialization logic as possible -- in
    case we're debugging issues with the initialization process or configuration
    (e.g. autodiscovery or import issues).
    """
    print(f"Request: {task.request!r}")
