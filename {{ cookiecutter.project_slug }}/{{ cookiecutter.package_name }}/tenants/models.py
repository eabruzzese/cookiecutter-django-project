from django.db import models
from django_extensions.db.fields import AutoSlugField
from django_tenants.models import DomainMixin, TenantMixin


class Tenant(TenantMixin):
    """A single tenant."""

    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from="name", unique=True)  # pyright: ignore[reportCallIssue]
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Automatically create the schema when the tenant is created.
    auto_create_schema = True

    domains: models.Manager["Domain"]


class Domain(DomainMixin):
    """A domain belonging to a tenant."""
