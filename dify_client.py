from __future__ import annotations
from dataclasses import dataclass
from typing import Any

import requests

from langfuse_support import (
    flush_langfuse,
    get_current_trace_url,
    start_observation,
    update_observation,
)
from settings import DifySettings


class DifyClientError(RuntimeError):
    def __init__(self, message: str, *, trace_url: str | None = None) -> None:
        super().__init__(message)
        self.trace_url = trace_url


@dataclass(frozen=True, slots=True)
class DifyReply:
    answer: str
    conversation_id: str | None
    message_id: str | None
    trace_url: str | None
    raw: dict[str, Any]


class DifyChatClient:
    def __init__(self, settings: DifySettings) -> None:
        self._settings = settings

    def send_message(
        self,
        text: str,
        *,
        conversation_id: str | None = None,
    ) -> DifyReply:
        prompt = (text or "").strip()
        if not prompt:
            raise DifyClientError("Input text is empty.")

        payload: dict[str, Any] = {
            "inputs": {},
            "query": prompt,
            "response_mode": self._settings.response_mode,
            "user": self._settings.user_id,
        }
        if conversation_id:
            payload["conversation_id"] = conversation_id

        observation_cm = start_observation(
            name="dify.chat.console",
            as_type="generation",
            input=payload,
            metadata={
                "provider": "dify",
                "base_url": self._settings.base_url,
                "response_mode": self._settings.response_mode,
            },
        )

        try:
            with observation_cm as observation:
                trace_url = get_current_trace_url()

                try:
                    response = requests.post(
                        f"{self._settings.base_url}/chat-messages",
                        headers={
                            "Authorization": f"Bearer {self._settings.api_key}",
                            "Content-Type": "application/json",
                        },
                        json=payload,
                        timeout=self._settings.timeout_seconds,
                    )
                    response.raise_for_status()
                except requests.exceptions.HTTPError as exc:
                    status_code = exc.response.status_code if exc.response is not None else None
                    body = exc.response.text if exc.response is not None else ""
                    message = f"Dify HTTP error {status_code}: {body[:500] or '<empty body>'}"
                    update_observation(
                        observation,
                        level="ERROR",
                        status_message=f"HTTP {status_code}",
                        output={"error_body": body[:500]},
                    )
                    raise DifyClientError(message, trace_url=trace_url) from exc
                except requests.exceptions.Timeout as exc:
                    update_observation(
                        observation,
                        level="ERROR",
                        status_message="Timeout",
                    )
                    raise DifyClientError("Dify request timed out.", trace_url=trace_url) from exc
                except requests.exceptions.RequestException as exc:
                    update_observation(
                        observation,
                        level="ERROR",
                        status_message="Network error",
                    )
                    raise DifyClientError(
                        f"Dify request failed: {exc}",
                        trace_url=trace_url,
                    ) from exc

                try:
                    data = response.json()
                except ValueError as exc:
                    update_observation(
                        observation,
                        level="ERROR",
                        status_message="Invalid JSON response",
                        output={"raw_response": response.text[:500]},
                    )
                    raise DifyClientError(
                        f"Dify returned invalid JSON: {response.text[:500]}",
                        trace_url=trace_url,
                    ) from exc

                answer = _extract_dify_answer(data)
                if answer is None:
                    update_observation(
                        observation,
                        level="ERROR",
                        status_message="Missing answer field",
                        output=data,
                    )
                    raise DifyClientError(
                        f"Dify response does not contain the 'answer' field: {data!r}",
                        trace_url=trace_url,
                    )
                if not answer:
                    error_message = _build_empty_answer_error_message(data)
                    update_observation(
                        observation,
                        level="ERROR",
                        status_message="Empty Dify answer",
                        output=data,
                    )
                    raise DifyClientError(error_message, trace_url=trace_url)

                update_observation(
                    observation,
                    output=answer,
                    metadata={
                        "conversation_id": _optional_text(data.get("conversation_id")) or "",
                        "message_id": _optional_text(data.get("message_id") or data.get("id")) or "",
                    },
                )
                return DifyReply(
                    answer=answer,
                    conversation_id=_optional_text(data.get("conversation_id")),
                    message_id=_optional_text(data.get("message_id") or data.get("id")),
                    trace_url=trace_url,
                    raw=data,
                )
        finally:
            flush_langfuse()


def _extract_dify_answer(data: Any) -> str | None:
    if not isinstance(data, dict):
        return None

    answer = data.get("answer")
    if answer is None:
        return None
    return str(answer).strip()


def _optional_text(value: Any) -> str | None:
    text = str(value or "").strip()
    return text or None


def _build_empty_answer_error_message(data: dict[str, Any]) -> str:
    mode = _optional_text(data.get("mode")) or "<unknown>"
    event = _optional_text(data.get("event")) or "<unknown>"
    conversation_id = _optional_text(data.get("conversation_id")) or "<unknown>"
    return (
        "Dify returned a successful response with an empty answer "
        f"(event={event}, mode={mode}, conversation_id={conversation_id}). "
        "Check the Dify app configuration. For Chatflow apps, each active branch "
        "should end with an Answer node. For Workflow apps, use the workflow API "
        "instead of /chat-messages."
    )
