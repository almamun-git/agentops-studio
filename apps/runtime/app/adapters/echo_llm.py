"""Local echo LLM adapter."""

from __future__ import annotations


class EchoLLMAdapter:
    """Returns the prompt/messages without remote calls."""

    async def generate(self, prompt: str, *, metadata: dict | None = None) -> str:
        return prompt

    async def chat(self, messages: list[dict], *, metadata: dict | None = None) -> dict:
        if not messages:
            return {"role": "assistant", "content": ""}
        return {"role": "assistant", "content": messages[-1].get("content", "")}
