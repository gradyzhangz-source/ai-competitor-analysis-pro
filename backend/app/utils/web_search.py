"""
搜索工具 — 支持 Tavily / Serper / 纯 LLM 回退
面试讲解重点：工具抽象层设计，优雅降级策略
"""
from __future__ import annotations
import json
import httpx
from abc import ABC, abstractmethod
from app.core.config import TAVILY_API_KEY, SERPER_API_KEY, SEARCH_RESULTS_PER_QUERY, REQUEST_TIMEOUT


class SearchProvider(ABC):
    @abstractmethod
    async def search(self, query: str, max_results: int = SEARCH_RESULTS_PER_QUERY) -> list[dict]:
        """返回 [{"title": ..., "url": ..., "snippet": ...}, ...]"""
        ...


class TavilySearch(SearchProvider):
    """Tavily — 专为 AI Agent 设计的搜索 API"""

    async def search(self, query: str, max_results: int = SEARCH_RESULTS_PER_QUERY) -> list[dict]:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            resp = await client.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": TAVILY_API_KEY,
                    "query": query,
                    "max_results": max_results,
                    "search_depth": "advanced",
                    "include_answer": True,
                },
            )
            resp.raise_for_status()
            data = resp.json()
            results = []
            if data.get("answer"):
                results.append({"title": "AI Summary", "url": "", "snippet": data["answer"]})
            for r in data.get("results", []):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("url", ""),
                    "snippet": r.get("content", ""),
                })
            return results


class SerperSearch(SearchProvider):
    """Serper — Google SERP API"""

    async def search(self, query: str, max_results: int = SEARCH_RESULTS_PER_QUERY) -> list[dict]:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            resp = await client.post(
                "https://google.serper.dev/search",
                headers={"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"},
                json={"q": query, "num": max_results},
            )
            resp.raise_for_status()
            data = resp.json()
            results = []
            if data.get("answerBox"):
                ab = data["answerBox"]
                results.append({
                    "title": ab.get("title", "Answer"),
                    "url": ab.get("link", ""),
                    "snippet": ab.get("snippet", ab.get("answer", "")),
                })
            for r in data.get("organic", []):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("link", ""),
                    "snippet": r.get("snippet", ""),
                })
            return results


class NoopSearch(SearchProvider):
    """无搜索 API 时的回退 — 返回空结果，Agent 将完全依赖 LLM 知识"""

    async def search(self, query: str, max_results: int = SEARCH_RESULTS_PER_QUERY) -> list[dict]:
        return []


def get_search_provider() -> SearchProvider:
    if TAVILY_API_KEY:
        return TavilySearch()
    if SERPER_API_KEY:
        return SerperSearch()
    return NoopSearch()


async def multi_query_search(queries: list[str], max_results_per_query: int = 5) -> dict[str, list[dict]]:
    """并发执行多个搜索查询，返回 {query: results}"""
    import asyncio

    provider = get_search_provider()
    tasks = {q: provider.search(q, max_results_per_query) for q in queries}

    results = {}
    for query, coro in tasks.items():
        try:
            results[query] = await coro
        except Exception as e:
            results[query] = [{"title": "Search Error", "url": "", "snippet": str(e)}]
    return results


def format_search_results(results: list[dict]) -> str:
    """将搜索结果格式化为 LLM 可读的文本"""
    if not results:
        return "（无搜索结果，请基于已有知识进行分析）"
    parts = []
    for i, r in enumerate(results, 1):
        parts.append(f"[{i}] {r['title']}\n    {r['snippet']}")
        if r.get("url"):
            parts.append(f"    来源: {r['url']}")
    return "\n\n".join(parts)
