# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Getting Started

### Prerequisites

- [uv](https://docs.astral.sh/uv/)
- [Docker](https://www.docker.com/) and Docker Compose

### Setup

```sh
bin/setup
```

This brings up all Docker Compose services and prints the URLs for the app and
admin tools:

| Service | URL |
|---|---|
| Django | http://localhost:8000 |
| pgAdmin | http://localhost:8054 |
| MailPit | http://localhost:8025 |
| Redis Commander | http://localhost:8063 |
| Flower (Celery) | http://localhost:8888 |
| RustFS Console | http://localhost:9001 |

### Running Tests

```sh
uv run pytest
```

### Code Quality

Pre-commit hooks are managed by [prek](https://github.com/j178/prek):

```sh
uv run prek run --all-files
```

## Architecture

### Multi-Tenancy — [django-tenants](https://github.com/django-tenants/django-tenants)

Each tenant gets an isolated PostgreSQL schema. Incoming requests are routed to
the correct schema via domain-based resolution. Shared data (users, tenants,
domains) lives in the `public` schema; tenant-specific data (feature flags,
dynamic config, sessions) lives in per-tenant schemas.

### Authentication — [django-allauth](https://github.com/pennersr/django-allauth)

Email-based login with a custom `User` model. Supports TOTP, recovery codes,
and WebAuthn for multi-factor authentication. Staff and superusers are required
to configure MFA via an enforcement middleware. Signup is protected by
reCAPTCHA and can be toggled on/off at runtime.

### Background Tasks — [Celery](https://github.com/celery/celery) + [tenant-schemas-celery](https://github.com/maciej-gol/tenant-schemas-celery)

Celery with a Redis broker and Django database result backend. The app uses a
custom `TenantAwareCeleryApp` so that tasks automatically execute within the
correct tenant's schema context. Periodic scheduling is handled by
`django-celery-beat`.

### Object Storage — [django-storages](https://github.com/jschneier/django-storages) (S3)

A custom `TenantAwareS3Boto3Storage` backend prefixes all uploads with the
current tenant's schema name, providing per-tenant isolation in a single S3
bucket. Local development uses [RustFS](https://github.com/nicholasgasior/rustfs)
as a MinIO-compatible mock.

### Dynamic Configuration — [django-constance](https://github.com/jazzband/django-constance)

Tenant-scoped runtime settings stored in the database. Used for controls like
toggling open registration without a deploy.

### Feature Flags — [django-waffle](https://github.com/django-waffle/django-waffle)

Database-backed feature flags, switches, and samples. Installed as a
tenant-scoped app, so flags can be configured independently per tenant.

### Frontend — [Tailwind CSS](https://tailwindcss.com/) + [HTMX](https://htmx.org/)

Tailwind v3 with forms, typography, aspect-ratio, and line-clamp plugins.
Compiled via a watch-mode Docker service during development. HTMX support is
provided via `django-htmx` middleware.

### Caching — [django-redis](https://github.com/jazzband/django-redis)

Redis-backed cache with tenant-aware cache keys (via `django-tenants`'s
`make_key` function) to prevent cross-tenant cache collisions.

### Additional Infrastructure

| Component | Library |
|---|---|
| Health checks | `django-health-check` (DB, cache, storage, Celery, disk, memory) |
| CORS | `django-cors-headers` |
| Static files | `whitenoise` with Brotli compression |
| Type checking | `basedpyright` with `django-stubs` |
| Linting | `ruff`, `django-upgrade`, `djhtml`, `shellcheck` |
| Pre-commit hooks | `prek` |
| Testing | `pytest` + `pytest-django` |
