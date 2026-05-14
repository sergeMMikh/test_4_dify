# test_4_dify

Minimal interactive Python app for debugging Dify without Instagram, PostgreSQL or the rest of the original project.

## What it does

- loads settings from a local `.env`;
- asks for user text in a loop;
- sends the text to Dify via `POST /chat-messages`;
- prints the Dify response;
- optionally sends traces to Langfuse;
- stops when you enter `EXIT`.

## Environment loading

The app checks these paths in order:

1. `DIFY_CONSOLE_ENV_PATH` if the environment variable is set
2. local `.env` in this directory
3. `C:\task-by-antipov\try_insta\.env`

Create a local `.env` from `.env.example` before running the app:

```powershell
Copy-Item .env.example .env
```

Then fill in the required secrets and any optional local overrides you want to use.

Required variables:

- `DIFY_API_KEY`

Optional variables:

- `DIFY_API_BASE_URL` default: `https://api.dify.ai/v1`
- `DIFY_RESPONSE_MODE` default: `blocking`
- `DIFY_TIMEOUT_SECONDS` default: `30`
- `DIFY_USER_ID` default: `interactive-console`
- `LANGFUSE_PUBLIC_KEY`
- `LANGFUSE_SECRET_KEY`
- `LANGFUSE_PORT` default in local setup: `3001`
- `LANGFUSE_BASE_URL` default in local setup: `http://localhost:3001`

## Langfuse

Local Langfuse services are defined in [docker-compose.yml](docker-compose.yml).

Before starting them, make sure your local `.env` contains valid Langfuse-related secrets.

Start them with:

```powershell
cd C:\task-by-antipov\test_4_dify
docker compose up -d
```

Then open:

```text
http://localhost:3001
```

Important:

- the compose file includes Langfuse headless initialization via `LANGFUSE_INIT_*`;
- you can use `LANGFUSE_INIT_*` to bootstrap an org, project and admin user on a fresh local setup;
- after `docker compose up -d`, wait until Langfuse becomes ready and then log in at `http://localhost:3001`;
- if you set bootstrap credentials in `.env`, log in with `LANGFUSE_INIT_USER_EMAIL` and `LANGFUSE_INIT_USER_PASSWORD`;
- if you change the project keys in `.env`, keep `LANGFUSE_PUBLIC_KEY` / `LANGFUSE_SECRET_KEY` and `LANGFUSE_INIT_PROJECT_PUBLIC_KEY` / `LANGFUSE_INIT_PROJECT_SECRET_KEY` in sync.

## Run

```powershell
cd C:\task-by-antipov\test_4_dify
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

## Stop

Type:

```text
EXIT
```
