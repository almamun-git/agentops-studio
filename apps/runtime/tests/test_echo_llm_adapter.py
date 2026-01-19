import pytest

from app.adapters.echo_llm import EchoLLMAdapter


@pytest.mark.asyncio
async def test_echo_llm_generate_returns_prompt():
    adapter = EchoLLMAdapter()
    result = await adapter.generate("hello")
    assert result == "hello"


@pytest.mark.asyncio
async def test_echo_llm_chat_returns_last_message():
    adapter = EchoLLMAdapter()
    result = await adapter.chat([{"role": "user", "content": "hi"}])
    assert result["content"] == "hi"
