---
last_mapped: 2026-05-14
---

# Stack

## Summary

This repository is a small Python console application for manually testing a Dify chat app without the larger upstream Instagram/PostgreSQL project. It loads local environment variables, sends chat messages to Dify, prints responses, and optionally records Langfuse observations.

## Languages And Runtime

- Python 3.10+ style code using `from __future__ import annotations`, dataclasses with `slots=True`, and `str | None` unions.
- PowerShell-oriented local setup documented in `README.md`.
- Docker Compose is used only for local Langfuse infrastructure, not for running the Python console itself.

## Python Dependencies

Defined in `requirements.txt`:

- `requests==2.32.5` - HTTP client used by `dify_client.py`.
- `python-dotenv==1.2.1` - loads `.env` files in `settings.py`.
- `langfuse==4.3.1` - optional tracing SDK used by `langfuse_support.py`.
- `isort==8.0.1` - formatting/import-order tool dependency, though no config file is present.

## Application Files

- `main.py` - CLI entry point and interactive loop.
- `settings.py` - environment discovery and typed settings.
- `dify_client.py` - Dify `/chat-messages` client and Dify response validation.
- `langfuse_support.py` - optional Langfuse wrapper helpers.
- `README.md` - setup, environment, Langfuse, and run instructions.
- `.env.example` - documented environment schema with placeholder secrets.

## Dify Artifacts

- `dify-DSL/try-insta-2.yml` - exported Dify advanced-chat DSL.
- `dify-DSL/try-insta-2_14.05.2026.yml` - dated Dify DSL snapshot.
- `questions/вопросы по Google таблицам.txt` - prompt/question notes, currently displayed as mojibake in the active shell encoding.

## Local Services

`docker-compose.yml` defines a Langfuse 3 self-hosting stack:

- `langfuse-web`
- `langfuse-worker`
- `postgres`
- `clickhouse`
- `minio`
- `redis`

The Python app does not depend on these services unless Langfuse environment variables are provided.

## Configuration

Runtime configuration comes from environment variables loaded in this order by `settings.py`:

1. `DIFY_CONSOLE_ENV_PATH`, if set.
2. Local `.env` in this project.
3. `../try_insta/.env`.

Required:

- `DIFY_API_KEY`

Optional:

- `DIFY_API_BASE_URL`, default `https://api.dify.ai/v1`
- `DIFY_RESPONSE_MODE`, default `blocking`
- `DIFY_TIMEOUT_SECONDS`, default `30`, clamped to at least 5 seconds
- `DIFY_USER_ID`, default `interactive-console`
- `LANGFUSE_PUBLIC_KEY`
- `LANGFUSE_SECRET_KEY`
- `LANGFUSE_BASE_URL` or `LANGFUSE_HOST`

## Tooling

No project-level config currently exists for:

- pytest
- ruff
- mypy
- black
- isort
- pre-commit
- CI

