"""
LLM 客户端 — 统一封装，支持多 Provider / 重试 / 结构化输出
面试讲解重点：抽象封装、重试机制、JSON Mode
"""
from __future__ import annotations
import json
import asyncio
from openai import AsyncOpenAI
from app.core.config import get_llm_config, MAX_RETRIES, TEMPERATURE, MAX_TOKENS, REQUEST_TIMEOUT


_client: AsyncOpenAI | None = None

def reset_client():
    global _client
    _client = None

def _get_client() -> AsyncOpenAI:
    global _client
    if _client is None:
        cfg = get_llm_config()
        _client = AsyncOpenAI(
            api_key=cfg["api_key"],
            base_url=cfg["base_url"],
            timeout=REQUEST_TIMEOUT,
        )
    return _client


async def chat_completion(
    system_prompt: str,
    user_prompt: str,
    temperature: float = TEMPERATURE,
    max_tokens: int = MAX_TOKENS,
    json_mode: bool = False,
) -> str:
    """发送一次 Chat Completion 请求，带指数退避重试"""
    client = _get_client()
    cfg = get_llm_config()

    kwargs: dict = {
        "model": cfg["model"],
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = await client.chat.completions.create(**kwargs)
            content = response.choices[0].message.content or ""
            return content.strip()
        except Exception as e:
            if attempt == MAX_RETRIES:
                raise RuntimeError(f"LLM 调用失败（重试 {MAX_RETRIES} 次后）: {e}") from e
            wait = 2 ** attempt
            await asyncio.sleep(wait)

    return ""


async def chat_completion_json(
    system_prompt: str,
    user_prompt: str,
    temperature: float = TEMPERATURE,
) -> dict:
    """请求结构化 JSON 输出并解析"""
    raw = await chat_completion(system_prompt, user_prompt, temperature=temperature, json_mode=True)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start != -1 and end > start:
            return json.loads(raw[start:end])
        raise ValueError(f"无法解析 JSON 响应: {raw[:200]}...")
