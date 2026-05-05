from __future__ import annotations

import logging
import os
from contextlib import nullcontext
from functools import lru_cache
from typing import Any


logger = logging.getLogger(__name__)

try:
    from langfuse import get_client
except ImportError:  # pragma: no cover - optional dependency guard
    get_client = None


@lru_cache(maxsize=1)
def get_langfuse_client() -> Any | None:
    if get_client is None:
        logger.warning("Langfuse SDK is not installed")
        return None

    public_key = (os.getenv("LANGFUSE_PUBLIC_KEY") or "").strip()
    secret_key = (os.getenv("LANGFUSE_SECRET_KEY") or "").strip()
    base_url = (
        os.getenv("LANGFUSE_BASE_URL")
        or os.getenv("LANGFUSE_HOST")
        or ""
    ).strip()

    if not public_key or not secret_key or not base_url:
        return None

    # Langfuse SDK expects LANGFUSE_BASE_URL in current versions.
    os.environ.setdefault("LANGFUSE_BASE_URL", base_url)

    try:
        return get_client()
    except Exception:
        logger.exception("Failed to initialize Langfuse client")
        return None


def start_observation(*, name: str, as_type: str, input: Any, metadata: dict[str, Any]):
    client = get_langfuse_client()
    if client is None:
        return nullcontext(None)

    try:
        return client.start_as_current_observation(
            name=name,
            as_type=as_type,
            input=input,
            metadata=metadata,
        )
    except Exception:
        logger.exception("Failed to start Langfuse observation")
        return nullcontext(None)


def update_observation(observation: Any, **kwargs: Any) -> None:
    if observation is None:
        return

    try:
        observation.update(**kwargs)
    except Exception:
        logger.exception("Failed to update Langfuse observation")


def get_current_trace_url() -> str | None:
    client = get_langfuse_client()
    if client is None:
        return None

    try:
        return client.get_trace_url()
    except Exception:
        logger.exception("Failed to get Langfuse trace URL")
        return None


def flush_langfuse() -> None:
    client = get_langfuse_client()
    if client is None:
        return

    try:
        client.flush()
    except Exception:
        logger.exception("Failed to flush Langfuse events")
