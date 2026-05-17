# cookiecutter-django-project

A [Cookiecutter](https://github.com/cookiecutter/cookiecutter) template for
production-ready, multi-tenant Django applications.

## What You Get

A fully containerized Django 6 project with schema-based multi-tenancy,
email-based authentication with MFA, background task processing, feature
flagging, and a Tailwind CSS frontend — all wired up and ready to deploy behind
ASGI with Uvicorn.

## Usage

### Prerequisites

- [uv](https://docs.astral.sh/uv/) (or `pipx` / `pip` to run `cookiecutter`)
- [Docker](https://www.docker.com/) and Docker Compose

### Generate a Project

```sh
uvx cookiecutter gh:eabruzzese/cookiecutter-django-project
```

You'll be prompted for:

| Variable | Description |
|---|---|
| `author_name` | Your full name |
| `author_email` | Your email address |
| `github_repository` | GitHub org/repo (e.g. `my-org/my-app`) |
| `project_name` | Human-readable name (e.g. `My App`) |
| `project_slug` | Auto-generated from project name (e.g. `my-app`) |
| `project_description` | Short description of the project |
| `project_license` | MIT, BSD, ISCL, Apache 2.0, or Proprietary |
| `package_name` | Python package name (e.g. `my_app`) |

After generation, the template automatically runs `uv lock`, `uv sync`,
initializes a git repository, and creates the initial commit.

### Start Developing

```sh
cd my-app
bin/setup
```

See the generated project's README for architecture documentation and
development instructions.

## Development (of this template)

To test the cookiecutter itself:

```sh
bin/test
```

This generates a project with default values, starts the services, and verifies
the health check endpoint responds.
