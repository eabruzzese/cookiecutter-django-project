from typing import TYPE_CHECKING

from django.contrib import admin

from {{ cookiecutter.package_name }}.tenants.models import Domain, Tenant

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from django.http import HttpRequest


class DomainInline(admin.TabularInline):
    """An inline admin class for the Domain model."""

    model = Domain
    extra = 0


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    """An admin class for the Tenant model."""

    search_fields = ("name", "slug", "domains__domain")
    list_display = ("name", "slug", "created_at", "updated_at", "_primary_domain")

    inlines = (DomainInline,)

    def has_module_permission(self, request: "HttpRequest") -> bool:
        """Check if the user has permission to access the Tenant model."""
        return not request.user.is_superuser

    def get_queryset(self, request: "HttpRequest") -> "QuerySet[Tenant]":
        """Get the queryset for the Tenant model."""

        return super().get_queryset(request).prefetch_related("domains")

    def _primary_domain(self, obj: Tenant) -> str | None:
        """Get the primary domain for a tenant."""
        return next((d.domain for d in obj.domains.all() if d.is_primary), None)
