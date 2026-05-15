from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_ENV_CANDIDATES = (
    PROJECT_ROOT / ".env",
    PROJECT_ROOT.parent / "try_insta" / ".env",
)


def main() -> None:
    configure_console_encoding()

    env_path = load_environment()
    settings = load_settings()
    conversation_id: str | None = None

    print(f"Loaded environment from: {env_path}")
    print(f"Dify base URL: {settings['base_url']}")
    print("Light mode: Langfuse and Docker services are not used.")
    print("Enter text for Dify. Type EXIT to stop.")

    while True:
        try:
            user_input = input("You> ").strip()
        except KeyboardInterrupt:
            print("\nInterrupted. Bye.")
            break
        except EOFError:
            print("\nEOF received. Bye.")
            break

        if user_input.upper() == "EXIT":
            print("Bye.")
            break

        if not user_input:
            print("Please enter some text or type EXIT.")
            continue

        try:
            reply = send_message(
                settings=settings,
                text=user_input,
                conversation_id=conversation_id,
            )
        except RuntimeError as exc:
            print(f"Dify error: {exc}")
            continue

        conversation_id = reply.get("conversation_id") or conversation_id
        print(f"Dify> {reply['answer']}")


def load_environment() -> Path:
    explicit_path = (os.getenv("DIFY_CONSOLE_ENV_PATH") or "").strip()
    if explicit_path:
        env_path = Path(explicit_path).expanduser().resolve()
        if not env_path.exists():
            raise FileNotFoundError(f"Configured env file was not found: {env_path}")
        load_dotenv(env_path, override=False)
        return env_path

    for candidate in DEFAULT_ENV_CANDIDATES:
        if candidate.exists():
            load_dotenv(candidate, override=False)
            return candidate

    raise FileNotFoundError(
        "No .env file found. Checked: "
        + ", ".join(str(path) for path in DEFAULT_ENV_CANDIDATES)
    )


def configure_console_encoding() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def load_settings() -> dict[str, Any]:
    api_key = read_required_env("DIFY_API_KEY")
    timeout_raw = (os.getenv("DIFY_TIMEOUT_SECONDS") or "30").strip()

    try:
        timeout_seconds = max(5, int(timeout_raw))
    except ValueError:
        timeout_seconds = 30

    return {
        "api_key": api_key,
        "base_url": (os.getenv("DIFY_API_BASE_URL") or "https://api.dify.ai/v1").strip().rstrip("/"),
        "response_mode": (os.getenv("DIFY_RESPONSE_MODE") or "blocking").strip() or "blocking",
        "timeout_seconds": timeout_seconds,
        "user_id": (os.getenv("DIFY_USER_ID") or "light-console").strip() or "light-console",
    }


def send_message(
    *,
    settings: dict[str, Any],
    text: str,
    conversation_id: str | None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "inputs": {},
        "query": text,
        "response_mode": settings["response_mode"],
        "user": settings["user_id"],
    }
    if conversation_id:
        payload["conversation_id"] = conversation_id

    try:
        response = requests.post(
            f"{settings['base_url']}/chat-messages",
            headers={
                "Authorization": f"Bearer {settings['api_key']}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=settings["timeout_seconds"],
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as exc:
        status_code = exc.response.status_code if exc.response is not None else None
        body = exc.response.text if exc.response is not None else ""
        raise RuntimeError(f"HTTP {status_code}: {body[:500] or '<empty body>'}") from exc
    except requests.exceptions.Timeout as exc:
        raise RuntimeError("Request timed out.") from exc
    except requests.exceptions.RequestException as exc:
        raise RuntimeError(f"Request failed: {exc}") from exc

    try:
        data = response.json()
    except ValueError as exc:
        raise RuntimeError(f"Invalid JSON response: {response.text[:500]}") from exc

    answer = str(data.get("answer") or "").strip()
    if not answer:
        raise RuntimeError(
            "Dify response does not contain a non-empty answer field: "
            + json.dumps(data, ensure_ascii=False)[:500]
        )

    return {
        "answer": answer,
        "conversation_id": optional_text(data.get("conversation_id")),
        "message_id": optional_text(data.get("message_id") or data.get("id")),
    }


def read_required_env(name: str) -> str:
    value = (os.getenv(name) or "").strip()
    if not value:
        raise RuntimeError(f"Required environment variable is missing: {name}")
    return value


def optional_text(value: Any) -> str | None:
    text = str(value or "").strip()
    return text or None


if __name__ == "__main__":
    main()
