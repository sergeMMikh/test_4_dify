---
last_mapped: 2026-05-14
---

# Concerns

## No Automated Tests

There are no tests around the most important behavior: environment loading, Dify request/response handling, and Langfuse failure tolerance. This makes small refactors risky because most correctness is currently verified manually.

Relevant files:

- `settings.py`
- `dify_client.py`
- `langfuse_support.py`
- `main.py`

## Potential Encoding Problem In Prompt Notes

`questions/вопросы по Google таблицам.txt` displays as mojibake in the current shell. If this file contains prompt logic or expected user-facing Russian text, future tooling may corrupt it or misunderstand it.

Recommended next step: identify the intended encoding and normalize to UTF-8 only after confirming the original text.

## Environment Fallback Can Surprise Users

`settings.py` falls back from local `.env` to `../try_insta/.env`. This is convenient, but can make the console use credentials or Dify app settings from a sibling project without the user noticing.

Relevant file:

- `settings.py`

Potential mitigation: print a stronger warning when the fallback env path is used, or require an explicit opt-in variable for cross-project env reuse.

## README Path Drift

`README.md` mentions `C:\task-by-antipov\test_4_dify` and `C:\task-by-antipov\try_insta\.env`, while the current workspace is `B:\git_projects\test_4_dify`. The behavior in code uses relative paths, but docs may confuse future runs.

Relevant files:

- `README.md`
- `settings.py`

## Dify API Mode Assumption

`dify_client.py` always calls `/chat-messages` and contains an error hint that Workflow apps should use the workflow API instead. The DSL files indicate an `advanced-chat` app today, so this is fine, but if the Dify app type changes, the console will fail by design.

Relevant files:

- `dify_client.py`
- `dify-DSL/try-insta-2.yml`

## Secret Hygiene

`.env` is ignored, and `.env.example` uses placeholders. Generated docs should avoid copying actual values from `.env`. The codebase map intentionally documents variable names and placeholder patterns only.

Relevant files:

- `.gitignore`
- `.env.example`
- `docker-compose.yml`

## Broad Exception Handling In Langfuse Adapter

`langfuse_support.py` intentionally swallows Langfuse SDK errors to avoid breaking the console. That is good for debugging Dify, but it can hide observability failures unless logs are watched.

Relevant file:

- `langfuse_support.py`

