"""
Strategy Agent — 战略建议生成
职责：基于分析结果，生成竞争定位、战略建议、风险评估
面试讲解重点：洞察→策略的转化逻辑、优先级排序机制
"""
from __future__ import annotations
import json

from app.core.base_agent import BaseAgent
from app.schemas.analysis import AnalysisState, StrategicRecommendation
from app.utils.llm_client import chat_completion, chat_completion_json
from app.prompts import strategy_prompts as prompts


class StrategyAgent(BaseAgent):
    name = "StrategyAgent"

    async def run(self, state: AnalysisState) -> AnalysisState:
        self.log(state, "开始生成战略建议...")

        our_profile_text = self._profile_to_text(state.our_profile)
        competitor_summary = self._competitor_summary(state)
        swot_text = self._swot_to_text(state)
        feature_summary = self._feature_summary(state)

        # Step 1: 竞争定位分析
        self.log(state, "分析竞争定位...")
        state.competitive_positioning = await self._positioning(
            state, our_profile_text, competitor_summary, swot_text, feature_summary
        )

        # Step 2: 战略行动建议
        self.log(state, "生成战略行动建议...")
        porters_summary = self._porters_to_text(state)
        state.recommendations = await self._recommendations(
            state, our_profile_text, porters_summary, swot_text, feature_summary
        )

        # Step 3: 风险评估
        self.log(state, "执行风险评估...")
        analysis_summary = (
            f"行业背景:\n{state.industry_context}\n\n"
            f"竞品概况:\n{competitor_summary}\n\n"
            f"SWOT 要点:\n{swot_text}\n\n"
            f"竞争定位:\n{state.competitive_positioning}"
        )
        state.risk_assessment = await self._risk_assessment(state, analysis_summary)

        # Step 4: 生成战略总结
        self.log(state, "生成战略总结...")
        state.strategic_summary = self._build_strategic_summary(state)

        self.log(state, f"战略建议生成完成，共 {len(state.recommendations)} 条建议")
        return state

    async def _positioning(
        self, state: AnalysisState, our_profile: str,
        competitor_summary: str, swot_text: str, feature_summary: str,
    ) -> str:
        prompt = prompts.COMPETITIVE_POSITIONING.format(
            our_profile=our_profile,
            competitor_summary=competitor_summary,
            swot_results=swot_text,
            feature_matrix_summary=feature_summary,
        )
        return await chat_completion(prompts.SYSTEM_PROMPT, prompt)

    async def _recommendations(
        self, state: AnalysisState, our_profile: str,
        porters_summary: str, swot_text: str, feature_summary: str,
    ) -> list[StrategicRecommendation]:
        prompt = prompts.STRATEGIC_RECOMMENDATIONS.format(
            our_profile=our_profile,
            industry_context=state.industry_context,
            porters_summary=porters_summary,
            swot_results=swot_text,
            positioning=state.competitive_positioning,
            feature_gaps=feature_summary,
            target_audience=state.request.target_audience,
        )
        data = await chat_completion_json(prompts.SYSTEM_PROMPT, prompt)
        recs = []
        for r in data.get("recommendations", []):
            recs.append(StrategicRecommendation(
                priority=r.get("priority", 99),
                category=r.get("category", "product"),
                title=r.get("title", ""),
                description=r.get("description", ""),
                rationale=r.get("rationale", ""),
                effort=r.get("effort", "medium"),
                impact=r.get("impact", "medium"),
                timeline=r.get("timeline", "medium"),
            ))
        recs.sort(key=lambda x: x.priority)
        return recs

    async def _risk_assessment(self, state: AnalysisState, analysis_summary: str) -> str:
        prompt = prompts.RISK_ASSESSMENT.format(analysis_summary=analysis_summary)
        return await chat_completion(prompts.SYSTEM_PROMPT, prompt)

    def _build_strategic_summary(self, state: AnalysisState) -> str:
        lines = ["## 战略总结\n"]
        lines.append(f"### 竞争定位\n{state.competitive_positioning}\n")
        if state.recommendations:
            lines.append("### Top 3 优先行动")
            for r in state.recommendations[:3]:
                lines.append(
                    f"**{r.priority}. {r.title}** [{r.category}]\n"
                    f"   {r.description}\n"
                    f"   投入: {r.effort} | 影响: {r.impact} | 周期: {r.timeline}\n"
                )
        return "\n".join(lines)

    @staticmethod
    def _profile_to_text(p) -> str:
        if p is None:
            return "（无数据）"
        return (
            f"{p.name}: {p.description}\n"
            f"优势: {'; '.join(p.strengths)}\n"
            f"劣势: {'; '.join(p.weaknesses)}\n"
            f"产品: {', '.join(p.key_products)}\n"
            f"定价: {p.pricing_model}"
        )

    @staticmethod
    def _competitor_summary(state: AnalysisState) -> str:
        return "\n".join(
            f"- **{cp.name}**: {cp.description}（{cp.tier.value}竞品）"
            for cp in state.competitor_profiles
        )

    @staticmethod
    def _swot_to_text(state: AnalysisState) -> str:
        parts = []
        for s in state.swot_results:
            parts.append(
                f"**{s.company}**\n"
                f"  S: {'; '.join(s.strengths[:3])}\n"
                f"  W: {'; '.join(s.weaknesses[:3])}\n"
                f"  O: {'; '.join(s.opportunities[:2])}\n"
                f"  T: {'; '.join(s.threats[:2])}"
            )
        return "\n\n".join(parts)

    @staticmethod
    def _porters_to_text(state: AnalysisState) -> str:
        if not state.porters:
            return "（未执行波特五力分析）"
        p = state.porters
        if isinstance(p, dict):
            parts = []
            for key in ["supplier_power", "buyer_power", "competitive_rivalry",
                        "threat_of_substitution", "threat_of_new_entry"]:
                item = p.get(key, {})
                if isinstance(item, dict):
                    parts.append(f"- {key}: {item.get('level', 'N/A')} — {item.get('analysis', '')[:100]}")
                else:
                    parts.append(f"- {key}: {item}")
            return "\n".join(parts)
        return str(p)

    @staticmethod
    def _feature_summary(state: AnalysisState) -> str:
        if not state.feature_matrix:
            return "（无功能对比数据）"
        lines = []
        for f in state.feature_matrix[:10]:
            scores = " | ".join(f"{k}: {v}" for k, v in f.scores.items())
            lines.append(f"- {f.feature_name}: {scores}")
        return "\n".join(lines)
