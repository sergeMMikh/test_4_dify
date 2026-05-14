---
last_mapped: 2026-05-14
---

# Structure

## Root Layout

- `main.py` - console entry point.
- `settings.py` - environment loading and typed settings.
- `dify_client.py` - Dify API client.
- `langfuse_support.py` - optional Langfuse SDK integration.
- `requirements.txt` - pinned Python dependencies.
- `README.md` - setup and usage guide.
- `docker-compose.yml` - local Langfuse service stack.
- `.env.example` - placeholder runtime configuration.
- `.gitignore` - ignores local secrets, virtualenvs, caches, logs, dumps, and editor files.
- `dify-DSL/` - exported Dify app YAML files.
- `questions/` - manual question/prompt notes.

## Module Boundaries

`main.py` depends on:

- `DifyChatClient`, `DifyClientError` from `dify_client.py`.
- `load_environment`, `load_dify_settings`, `load_langfuse_settings` from `settings.py`.

`dify_client.py` depends on:

- `requests`.
- Langfuse helper functions from `langfuse_support.py`.
- `DifySettings` from `settings.py`.

`langfuse_support.py` depends on:

- `langfuse.get_client`, if importable.
- Environment variables.

`settings.py` is independent except for `python-dotenv`.

## Naming Conventions

- Modules use simple snake_case names.
- Settings are immutable dataclasses: `DifySettings`, `LangfuseSettings`.
- API result and error types are explicit: `DifyReply`, `DifyClientError`.
- Private helpers use leading underscore: `_read_required_env`, `_optional_text`, `_extract_dify_answer`.

## Configuration File Locations

Environment lookup order is encoded in `settings.py`:

- `DIFY_CONSOLE_ENV_PATH`
- `.env`
- `../try_insta/.env`

Documentation in `README.md` references an older absolute path, `C:\task-by-antipov\try_insta\.env`, which is conceptually the same fallback but differs from the current repository path.

## Generated Or External Artifacts

- `.env` is local-only and ignored.
- `.venv/` is ignored.
- Docker volumes are named volumes declared in `docker-compose.yml`, not repository files.
- Dify DSL YAML files are source-controlled artifacts, not generated during app runtime.

## Missing Structure

No directories currently exist for:

- `tests/`
- `src/`
- `docs/`
- CI workflows
- packaging metadata

Given the project size, a flat structure is reasonable until tests or additional CLI commands are added.

