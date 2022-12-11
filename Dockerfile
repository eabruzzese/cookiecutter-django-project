##
# base
#
# A base image suitable for development. Assumes a volume will be mounted at
# /app.
#
FROM python:3.11-slim-bullseye AS base

ARG GIT_COMMIT_HASH

ENV PATH=$PATH:/root/.local/bin:/root/.poetry/bin \
    DEBIAN_FRONTEND=noninteractive \
    GIT_COMMIT_HASH=${GIT_COMMIT_HASH} \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=false \
    PIP_DISABLE_PIP_VERSION_CHECK=false \
    PAGER=cat

WORKDIR /app

RUN apt-get update \
 && apt-get install --assume-yes --no-install-recommends \
    curl \
    git \
    gnupg2 \
    lsb-release \
    openssh-client \
 && echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
 && curl -fsSL "https://www.postgresql.org/media/keys/ACCC4CF8.asc" | apt-key add - \
 && apt-get update \
 && apt-get install --assume-yes --no-install-recommends postgresql-client-14 \
 && rm -rf /var/lib/apt/lists/* \
 && apt-get autoremove --assume-yes \
 && apt-get clean --assume-yes \
 && rm -rf /tmp/*

# Install and configure poetry to manage our requirements.
#
# Since Poetry recommends installing via cURL, we verify the SHA1 of the
# install script before using it for security.
#
# Installation happens in a temporary directory that's cleaned up at the end of
# this step.
ENV POETRY_VERSION=1.2.2 \
    POETRY_INSTALLER_GIT_REF="be23be56c57efc142da94376737ee6ead4e89a46" \
    POETRY_INSTALLER_SHA1="3aa6bf1f8343fd110dd7acd809e4d8496842a8d7" \
    POETRY_VIRTUALENVS_CREATE=false
RUN echo "Installing poetry..." \
 && INSTALL_DIRECTORY="$(mktemp -d)" \
 && cd "$INSTALL_DIRECTORY" \
 && curl -sSL "https://raw.githubusercontent.com/python-poetry/install.python-poetry.org/$POETRY_INSTALLER_GIT_REF/install-poetry.py" > "install-poetry.py" \
 && printf "%s" "$POETRY_INSTALLER_SHA1 install-poetry.py" > "install-poetry.py.sha1" \
 && sha1sum --check "install-poetry.py.sha1" \
 && python "install-poetry.py" \
 && cd - \
 && rm -rf "$INSTALL_DIRECTORY"

# Install our production python dependencies.
COPY pyproject.toml poetry.lock /app/
RUN apt-get update \
 && apt-get install --assume-yes --no-install-recommends \
    build-essential \
    libffi-dev \
    libpq-dev \
 && poetry install --no-dev \
 && apt-get remove --assume-yes --no-install-recommends \
    build-essential \
    libffi-dev \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/* \
 && apt-get autoremove --assume-yes \
 && apt-get clean --assume-yes \
 && rm -rf /tmp/*


##
# dev
#
# An image suitable for running in development.
#
# Installs development-only dependencies, and does not copy the application code
# into the image (but instead assumes that a volume will be mounted containing
# the rest of the code).
#
FROM base AS dev

# Install all dependencies (including dev dependencies).
RUN poetry install

CMD ["./manage.py", "runserver_plus", "0.0.0.0:8000"]

EXPOSE 8000


##
# theme-build
#
# An ephemeral image for building the theme.
#
FROM node:lts-bullseye-slim AS theme-build

# Copy the whole intranet project (needed so that Tailwind can scan for its
# classes in the template files).
COPY ./intranet/. /build/intranet/.

# Copy the theme source.
COPY ./theme/. /build/theme/.

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
ENV GUNICORN_CMD_ARGS="--workers 3 --worker-connections=1000"

# Copy the application code and configuration.
COPY ./conf/. /app/conf/.
COPY ./manage.py /app/.
COPY ./intranet/. /app/intranet/.

# Copy the theme from the theme-build stage.
COPY --from=theme-build /build/theme/dist/css/theme.css /app/intranet/static/theme/css/theme.css

# Run collectstatic to colocate all of the required static assets. Note that we
# source the .env.example for this step, as the ./manage.py script requires that
# the settings file be valid.
COPY ./manage.py /app/.
COPY .env.example /tmp/.env.example
RUN ( \
  set -a \
  && . /tmp/.env.example \
  && ./manage.py collectstatic --no-input \
  && rm -f /tmp/.env.example \
)

CMD ["gunicorn", "--config=conf/gunicorn.conf.py", "intranet.asgi:application"]

EXPOSE 8000


##
# test
#
# An image used for testing in non-production environments (e.g., CI).
#
# Attempts to emulate the prod image as closely as possible, and includes
# dependencies required for testing.
#
FROM prod as test

# Install all dependencies (including dev and test dependencies).
RUN poetry install
