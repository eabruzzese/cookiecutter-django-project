from django.db import connection
from storages.backends.s3boto3 import S3Boto3Storage
from storages.utils import safe_join


class TenantAwareS3Boto3Storage(S3Boto3Storage):
    """A storage class that allows Django to store files in a S3 bucket per tenant."""

    _location: str = ""

    @property
    def location(self) -> str:
        """Return the location, prefixed with the tenant name."""
        return safe_join(connection.schema_name, self._location)

    @location.setter
    def location(self, value: str) -> None:
        """Set the location."""
        self._location = value
