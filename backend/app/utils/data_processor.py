"""
数据处理工具 — 清洗、去重、摘要
"""
from __future__ import annotations


def deduplicate_results(results: list[dict]) -> list[dict]:
    """基于 URL 去重搜索结果"""
    seen_urls: set[str] = set()
    deduped = []
    for r in results:
        url = r.get("url", "")
        if url and url in seen_urls:
            continue
        if url:
            seen_urls.add(url)
        deduped.append(r)
    return deduped


def merge_profiles(existing: dict, new_data: dict) -> dict:
    """合并两个 profile 字典，新数据补充空字段"""
    merged = {**existing}
    for key, value in new_data.items():
        if not merged.get(key) and value:
            merged[key] = value
        elif isinstance(value, list) and isinstance(merged.get(key), list):
            merged[key] = list({*merged[key], *value})
    return merged


def truncate_text(text: str, max_chars: int = 3000) -> str:
    """截断过长文本，保留信息密度最高的头尾"""
    if len(text) <= max_chars:
        return text
    half = max_chars // 2
    return text[:half] + "\n\n... [内容过长，已截断] ...\n\n" + text[-half:]
