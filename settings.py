from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_ENV_CANDIDATES = (
    PROJECT_ROOT / ".env",
    PROJECT_ROOT.parent / "try_insta" / ".env",
)


@dataclass(frozen=True, slots=True)
class DifySettings:
    api_key: str
    base_url: str
    response_mode: str
    timeout_seconds: int
    user_id: str


@dataclass(frozen=True, slots=True)
class LangfuseSettings:
    enabled: bool
    base_url: str | None
    public_key: str | None
    secret_key: str | None


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


def load_dify_settings() -> DifySettings:
    api_key = _read_required_env("DIFY_API_KEY")
    base_url = (os.getenv("DIFY_API_BASE_URL") or "https://api.dify.ai/v1").strip()
    response_mode = (os.getenv("DIFY_RESPONSE_MODE") or "blocking").strip() or "blocking"
    user_id = (os.getenv("DIFY_USER_ID") or "interactive-console").strip()

    timeout_raw = (os.getenv("DIFY_TIMEOUT_SECONDS") or "30").strip()
    try:
        timeout_seconds = max(5, int(timeout_raw))
    except ValueError:
        timeout_seconds = 30

    return DifySettings(
        api_key=api_key,
        base_url=base_url.rstrip("/"),
        response_mode=response_mode,
        timeout_seconds=timeout_seconds,
        user_id=user_id,
    )


def load_langfuse_settings() -> LangfuseSettings:
    public_key = _read_optional_env("LANGFUSE_PUBLIC_KEY")
    secret_key = _read_optional_env("LANGFUSE_SECRET_KEY")
    base_url = _read_optional_env("LANGFUSE_BASE_URL") or _read_optional_env("LANGFUSE_HOST")

    enabled = bool(public_key and secret_key and base_url)
    if base_url:
        base_url = base_url.rstrip("/")

    return LangfuseSettings(
        enabled=enabled,
        base_url=base_url,
        public_key=public_key,
        secret_key=secret_key,
    )


def _read_required_env(name: str) -> str:
    value = (os.getenv(name) or "").strip()
    if not value:
        raise RuntimeError(f"Required environment variable is missing: {name}")
    return value


def _read_optional_env(name: str) -> str | None:
    value = (os.getenv(name) or "").strip()
    return value or None
