---
last_mapped: 2026-05-14
---

# Testing

## Current State

No automated tests are present.

Missing:

- `tests/` directory.
- pytest configuration.
- unit tests for settings, Dify client behavior, and Langfuse fallback.
- integration tests or mocked HTTP tests.
- CI workflow.

## Manual Test Path

The documented test flow in `README.md` is manual:

1. Create virtual environment.
2. Install dependencies from `requirements.txt`.
3. Copy `.env.example` to `.env`.
4. Fill secrets.
5. Run `main.py`.
6. Type messages and inspect Dify responses.
7. Optionally start local Langfuse with `docker compose up -d` and inspect traces.

## High-Value Unit Tests To Add

`settings.py`:

- Loads explicit `DIFY_CONSOLE_ENV_PATH`.
- Falls back to local `.env`.
- Raises a clear error when no env file exists.
- Requires `DIFY_API_KEY`.
- Defaults and clamps timeout values.
- Enables Langfuse only when public key, secret key, and base URL are all present.

`dify_client.py`:

- Sends the expected JSON payload and bearer token.
- Preserves and sends `conversation_id`.
- Parses `answer`, `conversation_id`, and `message_id`.
- Raises `DifyClientError` for HTTP errors, timeout, network errors, invalid JSON, missing answer, and empty answer.
- Includes trace URL in errors when tracing is active.

`langfuse_support.py`:

- No-ops when SDK is missing or environment is incomplete.
- Does not crash when Langfuse SDK calls fail.

## Suggested Testing Tools

Given the current stack:

- `pytest` for test runner.
- `responses` or `requests-mock` for HTTP mocking.
- `monkeypatch` fixture for environment variables.

## Coverage Risks

The current code touches external services and local environment heavily. Without tests, the riskiest regressions are:

- Accidentally changing payload shape expected by Dify.
- Breaking optional Langfuse fallback.
- Loading the wrong `.env` file.
- Losing the user-friendly handling for empty or malformed Dify responses.

