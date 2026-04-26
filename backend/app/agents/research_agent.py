"""
Research Agent — 信息收集、竞品画像构建
职责：通过搜索工具收集竞品信息，构建结构化画像
面试讲解重点：搜索策略生成 → 并发搜索 → 结构化提取 → 画像构建
"""
from __future__ import annotations
import json

from app.core.base_agent import BaseAgent
from app.schemas.analysis import AnalysisState, CompetitorProfile, CompetitorTier
from app.utils.llm_client import chat_completion, chat_completion_json
from app.utils.web_search import multi_query_search, format_search_results, get_search_provider, NoopSearch
from app.utils.data_processor import deduplicate_results
from app.prompts import research_prompts as prompts


class ResearchAgent(BaseAgent):
    name = "ResearchAgent"

    async def run(self, state: AnalysisState) -> AnalysisState:
        req = state.request
        self.log(state, f"开始调研 {req.our_product} 及 {len(req.competitors)} 个竞品")

        # Step 1: 让 LLM 生成最优搜索查询
        self.log(state, "生成搜索查询策略...")
        search_plan = await self._generate_search_queries(state)

        # Step 2: 并发执行所有搜索
        all_queries = []
        for queries in search_plan.get("competitor_queries", {}).values():
            all_queries.extend(queries)
        all_queries.extend(search_plan.get("industry_queries", []))
        all_queries.append(f"{req.our_product} {req.our_description} 产品介绍 融资")

        provider = get_search_provider()
        if isinstance(provider, NoopSearch):
            self.log(state, "未配置搜索 API，将仅基于 LLM 知识进行分析")
            search_results = {q: [] for q in all_queries}
        else:
            self.log(state, f"并发执行 {len(all_queries)} 个搜索查询...")
            search_results = await multi_query_search(all_queries)

        # Step 3: 构建我方产品画像
        self.log(state, "构建我方产品画像...")
        our_search = format_search_results(
            search_results.get(all_queries[-1], [])
        )
        state.our_profile = await self._build_our_profile(state, our_search)

        # Step 4: 构建每个竞品的画像
        for comp_name in req.competitors:
            self.log(state, f"构建竞品画像: {comp_name}")
            comp_queries = search_plan.get("competitor_queries", {}).get(comp_name, [])
            comp_results = []
            for q in comp_queries:
                comp_results.extend(search_results.get(q, []))
            comp_results = deduplicate_results(comp_results)

            profile = await self._build_competitor_profile(
                state, comp_name, format_search_results(comp_results)
            )
            state.competitor_profiles.append(profile)

        # Step 5: 行业宏观分析
        self.log(state, "生成行业宏观分析...")
        industry_queries = search_plan.get("industry_queries", [])
        industry_results = []
        for q in industry_queries:
            industry_results.extend(search_results.get(q, []))
        state.industry_context = await self._build_industry_context(
            state, format_search_results(deduplicate_results(industry_results))
        )

        self.log(state, f"调研完成，共构建 {len(state.competitor_profiles)} 个竞品画像")
        return state

    async def _generate_search_queries(self, state: AnalysisState) -> dict:
        req = state.request
        competitor_list = "\n".join(f"- {c}" for c in req.competitors)
        prompt = prompts.GENERATE_SEARCH_QUERIES.format(
            our_product=req.our_product,
            our_description=req.our_description,
            industry=req.industry,
            competitor_list=competitor_list,
        )
        try:
            return await chat_completion_json(prompts.SYSTEM_PROMPT, prompt)
        except Exception:
            fallback = {
                "competitor_queries": {
                    c: [
                        f"{c} 产品功能 介绍",
                        f"{c} 融资 公司规模",
                        f"{c} 用户评价 竞争优势",
                    ]
                    for c in req.competitors
                },
                "industry_queries": [
                    f"{req.industry} 行业趋势 2024 2025",
                    f"{req.industry} 市场规模 竞争格局",
                ],
            }
            return fallback

    async def _build_our_profile(self, state: AnalysisState, search_results: str) -> CompetitorProfile:
        req = state.request
        prompt = prompts.BUILD_OUR_PROFILE.format(
            our_product=req.our_product,
            our_description=req.our_description,
            industry=req.industry,
            search_results=search_results,
        )
        data = await chat_completion_json(prompts.SYSTEM_PROMPT, prompt)
        return self._dict_to_profile(data)

    async def _build_competitor_profile(
        self, state: AnalysisState, name: str, search_results: str
    ) -> CompetitorProfile:
        req = state.request
        prompt = prompts.BUILD_COMPETITOR_PROFILE.format(
            competitor_name=name,
            our_product=req.our_product,
            our_description=req.our_description,
            industry=req.industry,
            search_results=search_results,
        )
        data = await chat_completion_json(prompts.SYSTEM_PROMPT, prompt)
        profile = self._dict_to_profile(data)
        return profile

    async def _build_industry_context(self, state: AnalysisState, search_results: str) -> str:
        prompt = prompts.INDUSTRY_CONTEXT.format(
            industry=state.request.industry,
            search_results=search_results,
        )
        return await chat_completion(prompts.SYSTEM_PROMPT, prompt)

    @staticmethod
    def _dict_to_profile(data: dict) -> CompetitorProfile:
        tier_map = {
            "direct": CompetitorTier.DIRECT,
            "indirect": CompetitorTier.INDIRECT,
            "potential": CompetitorTier.POTENTIAL,
        }
        return CompetitorProfile(
            name=data.get("name", ""),
            tier=tier_map.get(data.get("tier", ""), CompetitorTier.DIRECT),
            website=data.get("website", ""),
            description=data.get("description", ""),
            founding_year=data.get("founding_year"),
            headquarters=data.get("headquarters", ""),
            funding_stage=data.get("funding_stage", ""),
            funding_total=data.get("funding_total", ""),
            employee_count=data.get("employee_count", ""),
            key_products=data.get("key_products", []),
            target_users=data.get("target_users", ""),
            pricing_model=data.get("pricing_model", ""),
            tech_stack=data.get("tech_stack", []),
            strengths=data.get("strengths", []),
            weaknesses=data.get("weaknesses", []),
            recent_moves=data.get("recent_moves", []),
        )
