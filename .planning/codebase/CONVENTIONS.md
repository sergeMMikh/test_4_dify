---
last_mapped: 2026-05-14
---

# Conventions

## Python Style

- All Python files use `from __future__ import annotations`.
- Standard library imports are separated from third-party and local imports.
- Dataclasses are frozen and use `slots=True` for settings/reply objects.
- Type hints are used consistently for public functions and helpers.
- Optional values use modern union syntax such as `str | None`.

## Error Handling

- External API errors are normalized into `DifyClientError` in `dify_client.py`.
- Optional Langfuse failures are logged and swallowed in `langfuse_support.py`.
- `main.py` catches user-exit conditions (`KeyboardInterrupt`, `EOFError`) and domain errors, then keeps the console experience simple.

## Configuration Pattern

- Environment access is centralized in `settings.py` except for Langfuse SDK initialization, where `langfuse_support.py` reads keys directly.
- Required and optional environment readers are explicit helper functions.
- Defaults are set close to the settings object construction.

## Observability Pattern

- `start_observation()` returns a context manager in all cases: either a Langfuse context or `nullcontext(None)`.
- `update_observation()` safely no-ops for missing observations.
- `flush_langfuse()` is called in `finally` after each Dify request.

## CLI UX Pattern

- The console prints loaded environment path and current Dify base URL.
- It uses `You>` and `Dify>` prefixes.
- It treats blank input as recoverable.
- It uses `EXIT` as the explicit quit command.

## Documentation Style

- `README.md` is practical and command-oriented.
- Setup commands are PowerShell-flavored.
- `.env.example` includes placeholders rather than real secrets.

## Import Ordering

`requirements.txt` includes `isort`, but there is no `pyproject.toml`, `.isort.cfg`, or other formatter configuration. Current files are already mostly organized, though `dify_client.py` has no blank line between `from __future__ import annotations` and the following import.

## Encoding

The repository includes Russian text in `questions/вопросы по Google таблицам.txt`, but the shell displayed mojibake when reading it. Treat encoding carefully for prompt files and avoid blind rewrites unless the intended encoding is confirmed.

