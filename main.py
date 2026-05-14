from __future__ import annotations

import logging

from dify_client import DifyChatClient, DifyClientError
from settings import load_dify_settings, load_environment, load_langfuse_settings


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    env_path = load_environment()
    settings = load_dify_settings()
    langfuse_settings = load_langfuse_settings()
    client = DifyChatClient(settings)
    conversation_id: str | None = None

    print(f"Loaded environment from: {env_path}")
    print(f"Dify base URL: {settings.base_url}")
    if langfuse_settings.enabled:
        print(f"Langfuse enabled: {langfuse_settings.base_url}")
    else:
        print("Langfuse disabled: set LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY and LANGFUSE_BASE_URL")
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
            reply = client.send_message(
                user_input,
                conversation_id=conversation_id,
            )
        except DifyClientError as exc:
            print(f"Dify error: {exc}")
            continue

        conversation_id = reply.conversation_id or conversation_id
        print(f"Dify> {reply.answer}")


if __name__ == "__main__":
    main()
