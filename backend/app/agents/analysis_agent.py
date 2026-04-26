"""
Analysis Agent — 多框架深度分析
职责：基于 Research 阶段数据，执行 SWOT / 五力 / 功能对比 / 商业模式等分析
面试讲解重点：多框架并行、结构化输出解析、分析深度控制
"""
from __future__ import annotations
import json

from app.core.base_agent import BaseAgent
from app.schemas.analysis import AnalysisState, AnalysisDepth, SWOTResult, FeatureComparison
from app.utils.llm_client import chat_completion, chat_completion_json
from app.prompts import analysis_prompts as prompts


class AnalysisAgent(BaseAgent):
    name = "AnalysisAgent"

    async def run(self, state: AnalysisState) -> AnalysisState:
        self.log(state, "开始多框架分析...")

        profiles_text = self._format_all_profiles(state)
        competitor_summary = self._format_competitor_summary(state)

        # ── 产品功能对比矩阵（所有深度都执行）──
        self.log(state, "生成产品功能对比矩阵...")
        state.feature_matrix = await self._feature_matrix(state, profiles_text)

        # ── SWOT 分析（所有深度都执行）──
        self.log(state, "执行 SWOT 分析...")
        if state.our_profile:
            our_swot = await self._swot_analysis(
                state, self._profile_to_text(state.our_profile),
                state.our_profile.name, competitor_summary,
            )
            state.swot_results.append(our_swot)

        for cp in state.competitor_profiles:
            swot = await self._swot_analysis(
                state, self._profile_to_text(cp), cp.name, competitor_summary,
            )
            state.swot_results.append(swot)

        # ── 波特五力（standard + deep）──
        if state.request.depth in (AnalysisDepth.STANDARD, AnalysisDepth.DEEP):
            self.log(state, "执行波特五力分析...")
            state.porters = await self._porters_five_forces(state, profiles_text)

        # ── 商业模式对比（standard + deep）──
        if state.request.depth in (AnalysisDepth.STANDARD, AnalysisDepth.DEEP):
            self.log(state, "执行商业模式对比...")
            state.business_model_analysis = await self._business_model(state, profiles_text)

        # ── 用户体验 + 技术对比（deep only）──
        if state.request.depth == AnalysisDepth.DEEP:
            self.log(state, "执行用户体验对比...")
            state.ux_comparison = await self._ux_comparison(state, profiles_text)
            self.log(state, "执行技术架构对比...")
            state.tech_comparison = await self._tech_comparison(state, profiles_text)

        self.log(state, "多框架分析完成")
        return state

    # ── 功能对比 ──
    async def _feature_matrix(self, state: AnalysisState, profiles_text: str) -> list[FeatureComparison]:
        prompt = prompts.PRODUCT_FEATURE_MATRIX.format(
            our_profile=self._profile_to_text(state.our_profile) if state.our_profile else "",
            competitor_profiles=profiles_text,
            industry=state.request.industry,
            focus_areas=", ".join(state.request.focus_areas) if state.request.focus_areas else "全面对比",
        )
        data = await chat_completion_json(prompts.SYSTEM_PROMPT, prompt)
        features = []
        for dim in data.get("dimensions", []):
            for feat in dim.get("features", []):
                features.append(FeatureComparison(
                    feature_name=f"[{dim.get('category', '')}] {feat.get('feature_name', '')}",
                    scores=feat.get("scores", {}),
                ))
        return features

    # ── SWOT ──
    async def _swot_analysis(
        self, state: AnalysisState, profile_text: str, name: str, competitor_summary: str
    ) -> SWOTResult:
        prompt = prompts.SWOT_ANALYSIS.format(
            company_profile=profile_text,
            industry_context=state.industry_context,
            competitor_summary=competitor_summary,
            company_name=name,
        )
        data = await chat_completion_json(prompts.SYSTEM_PROMPT, prompt)
        return SWOTResult(
            company=data.get("company", name),
            strengths=data.get("strengths", []),
            weaknesses=data.get("weaknesses", []),
            opportunities=data.get("opportunities", []),
            threats=data.get("threats", []),
        )

    # ── 波特五力 ──
    async def _porters_five_forces(self, state: AnalysisState, profiles_text: str) -> dict:
        prompt = prompts.PORTERS_FIVE_FORCES.format(
            industry=state.request.industry,
            industry_context=state.industry_context,
            all_profiles_summary=profiles_text,
        )
        return await chat_completion_json(prompts.SYSTEM_PROMPT, prompt)

    # ── 商业模式 ──
    async def _business_model(self, state: AnalysisState, profiles_text: str) -> str:
        prompt = prompts.BUSINESS_MODEL_COMPARISON.format(all_profiles=profiles_text)
        return await chat_completion(prompts.SYSTEM_PROMPT, prompt)

    # ── 用户体验 ──
    async def _ux_comparison(self, state: AnalysisState, profiles_text: str) -> str:
        prompt = prompts.UX_COMPARISON.format(all_profiles=profiles_text)
        return await chat_completion(prompts.SYSTEM_PROMPT, prompt)

    # ── 技术对比 ──
    async def _tech_comparison(self, state: AnalysisState, profiles_text: str) -> str:
        prompt = prompts.TECH_COMPARISON.format(all_profiles=profiles_text)
        return await chat_completion(prompts.SYSTEM_PROMPT, prompt)

    # ── 辅助方法 ──
    @staticmethod
    def _profile_to_text(p) -> str:
        if p is None:
            return "（无数据）"
        lines = [
            f"**{p.name}**",
            f"- 定位: {p.description}",
            f"- 目标用户: {p.target_users}",
            f"- 核心产品: {', '.join(p.key_products)}",
            f"- 融资阶段: {p.funding_stage}",
            f"- 定价模式: {p.pricing_model}",
            f"- 技术栈: {', '.join(p.tech_stack)}",
            f"- 优势: {'; '.join(p.strengths)}",
            f"- 劣势: {'; '.join(p.weaknesses)}",
            f"- 近期动态: {'; '.join(p.recent_moves)}",
        ]
        return "\n".join(lines)

    def _format_all_profiles(self, state: AnalysisState) -> str:
        parts = []
        if state.our_profile:
            parts.append(f"## 我方产品\n{self._profile_to_text(state.our_profile)}")
        for cp in state.competitor_profiles:
            parts.append(f"## 竞品: {cp.name}\n{self._profile_to_text(cp)}")
        return "\n\n".join(parts)

    def _format_competitor_summary(self, state: AnalysisState) -> str:
        parts = []
        for cp in state.competitor_profiles:
            parts.append(f"- {cp.name}: {cp.description}（优势: {'; '.join(cp.strengths[:2])}）")
        return "\n".join(parts)
