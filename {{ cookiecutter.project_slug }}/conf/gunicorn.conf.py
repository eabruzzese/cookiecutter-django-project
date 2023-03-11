import logging
import multiprocessing
import os
from pathlib import Path

from uvicorn.workers import UvicornWorker as BaseUvicornWorker


class UvicornWorker(BaseUvicornWorker):
    """A customized Uvicorn worker class."""

    CONFIG_KWARGS = {"loop": "auto", "http": "auto", "lifespan": "off"}


logger = logging.getLogger(__name__)


def _detect_workers() -> int:
    """Return the optimal number of workers for the detected hardware.

    Examples:
        * On a non-Unix OS (i.e. no support for `os.sched_getaffinity`, like
          MacOS) that returns 8 for the number of CPU cores, the function would
          return (2 * 8 cores) + 1 = 17 workers.
        * On a Unix OS (i.e. with support for `os.sched_getaffinity`, like
          Linux) that returns {1} as the set of usable CPU cores (i.e.,
          1 core), the function would return (2 * 1 cores) + 1 = 3 workers.
        * On any system that detects zero CPU cores (i.e., a misconfigured Linux
          distribution, or an environment with insufficient privileges to
          retrieve hardware information), the function would return 2 (the
          minimum).
    """
    try:
        cpu_cores = len(os.sched_getaffinity(0))
    except AttributeError:
        cpu_cores = multiprocessing.cpu_count()

    workers = max((2 * cpu_cores) + 1, 2)

    if workers < 3:
        logger.warning(
            "The number of Gunicorn workers is less than 3, which means that "
            "automatic detection of CPU cores has failed. You may want to set "
            "the number of workers manually via the GUNICORN_WORKERS "
            "environment variable while you investigate."
        )

    return workers


# Gunicorn configuration variables
#
# See https://docs.gunicorn.org/en/stable/settings.html#settings
#
loglevel = os.getenv("GUNICORN_LOGLEVEL", os.getenv("LOG_LEVEL", "info"))
workers = os.getenv("GUNICORN_WORKERS") or _detect_workers()
worker_class = os.getenv(
    "GUNICORN_WORKER_CLASS", f"{UvicornWorker.__module__}.{UvicornWorker.__qualname__}"
)
bind = os.getenv("GUNICORN_BIND", f"0.0.0.0:{os.getenv('PORT', '8000')}")
errorlog = os.getenv("GUNICORN_ERRORLOG", "-") or None
accesslog = os.getenv("GUNICORN_ACCESSLOG", "-") or None
graceful_timeout = int(os.getenv("GUNICORN_GRACEFUL_TIMEOUT", os.getenv("IDLE_TIMEOUT", "120")))
timeout = int(os.getenv("GUNICORN_TIMEOUT", os.getenv("IDLE_TIMEOUT", "120")))
keepalive = int(os.getenv("GUNICORN_KEEPALIVE", "5"))
max_requests = int(os.getenv("GUNICORN_MAX_REQUESTS", "0"))
max_requests_jitter = int(os.getenv("GUNICORN_MAX_REQUESTS_JITTER", max_requests * 0.1))
statsd_host = os.getenv("GUNICORN_STATSD_HOST", "localhost:8125")
statsd_prefix = os.getenv("GUNICORN_STATSD_PREFIX", "gunicorn")
preload_app = os.getenv("GUNICORN_PRELOAD_APP", "True").lower() == "true"
worker_tmp_dir = "/dev/shm" if Path("/dev/shm").exists() else None
