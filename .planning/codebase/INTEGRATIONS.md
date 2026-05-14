---
last_mapped: 2026-05-14
---

# Integrations

## Dify

Primary external integration. `dify_client.py` posts chat requests to:

- `POST {DIFY_API_BASE_URL}/chat-messages`

The request payload includes:

- `inputs: {}`
- `query`
- `response_mode`
- `user`
- optional `conversation_id`

Authentication uses:

- `Authorization: Bearer {DIFY_API_KEY}`

Response handling expects JSON with:

- `answer`
- optional `conversation_id`
- optional `message_id` or `id`

The client raises `DifyClientError` for empty input, HTTP errors, timeouts, network failures, invalid JSON, missing `answer`, and empty `answer`.

## Langfuse SDK

Optional observability integration implemented in `langfuse_support.py`.

Activation requires all of:

- `LANGFUSE_PUBLIC_KEY`
- `LANGFUSE_SECRET_KEY`
- `LANGFUSE_BASE_URL` or `LANGFUSE_HOST`

`dify_client.py` wraps every Dify request in a Langfuse observation named `dify.chat.console` with type `generation`. It records request payload, provider metadata, response output, and error metadata. Trace URLs are surfaced back through `DifyReply.trace_url` and `DifyClientError.trace_url`.

## Self-Hosted Langfuse Services

`docker-compose.yml` provisions local Langfuse dependencies:

- PostgreSQL 17 for Langfuse relational storage.
- ClickHouse for Langfuse event analytics.
- MinIO for event/media object storage.
- Redis 7 for queue/cache support.
- Langfuse web and worker containers.

The compose file uses environment variables from `.env`, including bootstrap variables such as `LANGFUSE_INIT_ORG_NAME`, `LANGFUSE_INIT_PROJECT_NAME`, and `LANGFUSE_INIT_USER_EMAIL`.

## Filesystem Integration

`settings.py` supports reusing an environment file from another local project:

- `../try_insta/.env`

This is convenient for debugging against the original project, but it also means local runs can silently use configuration from outside this repository if local `.env` is missing.

## Dify DSL

The `dify-DSL/` directory stores exported app definitions. These files are not loaded by the Python runtime, but they are important integration artifacts because they describe the Dify workflow being tested.

## External Network Calls

- Dify API over HTTPS by default.
- Langfuse API at `LANGFUSE_BASE_URL` when enabled.
- Docker images pulled from `docker.io`, `cgr.dev`, and related registries when starting the local stack.

## Webhooks And Auth Providers

No inbound webhooks, OAuth providers, or application user auth are implemented in the Python app. All authentication is service-token based through environment variables.

