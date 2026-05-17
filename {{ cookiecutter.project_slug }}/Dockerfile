##
# base
#
# A base image suitable for all stages.
#
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS base

ARG GIT_COMMIT_HASH

ENV PATH=/opt/venv/bin:$PATH:/root/.local/bin \
    DEBIAN_FRONTEND=noninteractive \
    GIT_COMMIT_HASH=${GIT_COMMIT_HASH} \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=false \
    PIP_DISABLE_PIP_VERSION_CHECK=false \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    PAGER=cat

WORKDIR /app

RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update \
 && apt-get install --assume-yes --no-install-recommends \
    curl \
    git \
    gnupg2 \
    lsb-release \
    openssh-client \
 && echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
 && curl -fsSL "https://www.postgresql.org/media/keys/ACCC4CF8.asc" | apt-key add - \
 && apt-get update \
 && apt-get install --assume-yes --no-install-recommends postgresql-client-16 \
 && apt-get remove --assume-yes --no-install-recommends \
    curl \
    gnupg2 \
    lsb-release \
 && rm -rf /var/lib/apt/lists/* \
 && apt-get autoremove --assume-yes \
 && apt-get clean --assume-yes \
 && rm -rf /tmp/*


##
# deps
#
# Installs production Python dependencies (no project source).
#
# Build tools are installed temporarily for packages with C extensions and
# removed afterwards to keep the layer small.
#
FROM base AS deps

COPY pyproject.toml /app/
RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/root/.cache/uv \
    apt-get update \
 && apt-get install --assume-yes --no-install-recommends \
    build-essential \
    libffi-dev \
    libpq-dev \
 && uv sync --no-dev --no-install-project \
 && apt-get remove --assume-yes --no-install-recommends \
    build-essential \
    libffi-dev \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/* \
 && apt-get autoremove --assume-yes \
 && apt-get clean --assume-yes \
 && rm -rf /tmp/*


##
# dev-deps
#
# Extends deps with development and testing dependencies (no project source).
#
# Dev packages are pure Python, so no build tools are required.
#
FROM deps AS dev-deps

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-install-project


##
# dev
#
# An image suitable for running in development.
#
# Does not copy the application code into the image (assumes a volume mount).
#
FROM base AS dev

COPY --from=dev-deps /opt/venv /opt/venv

CMD ["./manage.py", "runserver_plus", "0.0.0.0:8000"]

EXPOSE 8000


##
# theme-build
#
# An ephemeral image for building the theme.
#
FROM node:lts-bullseye-slim AS theme-build

# Copy the whole project (needed so that Tailwind can scan for its classes in
# the template files).
COPY ./{{ cookiecutter.package_name }}/ /build/{{ cookiecutter.package_name }}/

# Copy the theme source.
COPY ./theme/ /build/theme/

# Run the production theme build.
WORKDIR /build/theme
RUN yarn --silent run optimize

ENTRYPOINT ["yarn", "run"]


##
# prod
#
# A production-ready image.
#
# Includes production-only dependencies and configuration.
#
FROM base AS prod
ENV UVICORN_HOST=0.0.0.0 \
    UVICORN_PORT=8000 \
    UVICORN_WORKERS=3

COPY --from=deps /opt/venv /opt/venv

# Copy the application code and configuration.
COPY ./manage.py /app/
COPY ./{{ cookiecutter.package_name }}/ /app/{{ cookiecutter.package_name }}/

# Copy the theme from the theme-build stage.
COPY --from=theme-build /build/theme/dist/css/theme.css /app/{{ cookiecutter.package_name }}/static/theme/css/

# Run collectstatic to colocate all of the required static assets. Note that we
# source the .env.example for this step, as the ./manage.py script requires that
# the settings file be valid.
COPY .env.example /tmp/.env.example
RUN ( \
  set -a \
  && . /tmp/.env.example \
  && ./manage.py collectstatic --no-input \
  && rm -f /tmp/.env.example \
)

CMD ["uvicorn", "{{ cookiecutter.package_name }}.asgi:application"]

EXPOSE 8000


##
# test
#
# An image used for testing in non-production environments (e.g., CI).
#
# Attempts to emulate the prod image as closely as possible, and includes
# dependencies required for testing.
#
FROM prod AS test

# Swap in the full dev venv, then do a fast project-only sync now that the
# source is present.
COPY --from=dev-deps /opt/venv /opt/venv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync
