---
last_mapped: 2026-05-14
---

# Architecture

## Shape

The codebase is a compact layered console utility:

- CLI orchestration in `main.py`.
- Typed configuration in `settings.py`.
- Dify API boundary in `dify_client.py`.
- Optional observability adapter in `langfuse_support.py`.

There is no web server, database access layer, background job system, or internal package structure.

## Entry Point

`main.py` is the executable entry point:

1. Configure Python logging.
2. Load `.env` via `load_environment()`.
3. Build `DifySettings` and `LangfuseSettings`.
4. Create `DifyChatClient`.
5. Start an input loop until `EXIT`, `KeyboardInterrupt`, or `EOFError`.
6. Maintain a single `conversation_id` across messages.
7. Print Dify answers and trace URLs.

## Data Flow

1. User types text into the console.
2. `main.py` strips and validates non-empty input.
3. `DifyChatClient.send_message()` builds a Dify payload.
4. `langfuse_support.start_observation()` returns a real Langfuse observation context or `nullcontext(None)`.
5. `requests.post()` sends the payload to Dify.
6. `dify_client.py` validates HTTP status, JSON shape, and the `answer` field.
7. `DifyReply` returns normalized response data to `main.py`.
8. `main.py` updates the conversation id and prints output.
9. `flush_langfuse()` runs in `finally` for every request.

## Error Handling

The Dify boundary converts low-level failures into `DifyClientError`:

- HTTP status failures include status code and up to 500 characters of response body.
- Timeouts become `Dify request timed out.`
- Other request exceptions include the original exception text.
- Invalid JSON and missing/empty answer get domain-specific messages.

`main.py` catches only `DifyClientError` during message sending, prints a friendly error, and continues the loop.

## Observability Pattern

Langfuse support is deliberately optional:

- Import failure is tolerated in `langfuse_support.py`.
- Missing keys return `None`.
- Langfuse operation failures are logged and degrade to no tracing.

The client code does not need conditionals around tracing because helper functions accept `None` observations.

## State Model

There is no persisted application state. Runtime state is limited to:

- Process environment.
- Current Dify `conversation_id` held in `main.py`.
- Cached Langfuse client via `@lru_cache(maxsize=1)`.

## Deployment Model

The Python console is run directly from a virtual environment. The Docker Compose stack is for local Langfuse only and is not a deployment wrapper for the app.

