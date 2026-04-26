"""
Report Agent — 报告生成与导出
职责：将所有分析结果整合为专业的 Markdown 报告
面试讲解重点：信息整合能力、报告结构设计、输出质量控制
"""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

from app.core.base_agent import BaseAgent
from app.schemas.analysis import AnalysisState
from app.utils.llm_client import chat_completion
from app.prompts import report_prompts as prompts
from app.core.config import OUTPUT_DIR


class ReportAgent(BaseAgent):
    name = "ReportAgent"

    async def run(self, state: AnalysisState) -> AnalysisState:
        self.log(state, "开始生成分析报告...")

        # Step 1: 生成 Executive Summary
        self.log(state, "撰写 Executive Summary...")
        state.executive_summary = await self._executive_summary(state)

        # Step 2: 准备各模块文本
        self.log(state, "整合各模块分析结果...")
        modules = self._prepare_modules(state)

        # Step 3: 生成完整报告
        self.log(state, "编排完整报告...")
        state.final_report_md = await self._compile_report(state, modules)

        # Step 4: 导出文件
        output_path = self._export(state)
        self.log(state, f"报告已导出: {output_path}")

        return state

    async def _executive_summary(self, state: AnalysisState) -> str:
        key_findings = []
        if state.competitive_positioning:
            key_findings.append(f"竞争定位:\n{state.competitive_positioning[:300]}")
        if state.recommendations:
            top3 = state.recommendations[:3]
            recs_text = "\n".join(f"- {r.title}: {r.description[:60]}" for r in top3)
            key_findings.append(f"Top 建议:\n{recs_text}")
        if state.risk_assessment:
            key_findings.append(f"风险要点:\n{state.risk_assessment[:200]}")

        prompt = prompts.EXECUTIVE_SUMMARY.format(
            our_product=state.request.our_product,
            industry=state.request.industry,
            competitor_count=len(state.competitor_profiles),
            depth=state.request.depth.value,
            key_findings="\n\n".join(key_findings),
        )
        return await chat_completion(prompts.SYSTEM_PROMPT, prompt)

    def _prepare_modules(self, state: AnalysisState) -> dict:
        """把 state 中的各模块数据转为报告文本"""
        # 竞品画像
        profiles_parts = []
        for cp in state.competitor_profiles:
            profiles_parts.append(self._profile_to_report_section(cp))
        competitor_profiles_text = "\n\n".join(profiles_parts)

        # 功能对比矩阵
        feature_lines = ["| 功能点 | " + " | ".join(
            cp.name for cp in ([state.our_profile] if state.our_profile else []) + state.competitor_profiles
        ) + " |"]
        feature_lines.append("|" + "---|" * (len(state.competitor_profiles) + 2))
        for f in state.feature_matrix:
            row = f"| {f.feature_name} |"
            for name in ([state.our_profile.name] if state.our_profile else []) + [cp.name for cp in state.competitor_profiles]:
                row += f" {f.scores.get(name, 'N/A')} |"
            feature_lines.append(row)
        feature_matrix_text = "\n".join(feature_lines) if state.feature_matrix else "（未生成功能对比）"

        # SWOT
        swot_parts = []
        for s in state.swot_results:
            swot_parts.append(
                f"### {s.company}\n"
                f"**优势 (S):** {'; '.join(s.strengths)}\n\n"
                f"**劣势 (W):** {'; '.join(s.weaknesses)}\n\n"
                f"**机会 (O):** {'; '.join(s.opportunities)}\n\n"
                f"**威胁 (T):** {'; '.join(s.threats)}"
            )
        swot_text = "\n\n".join(swot_parts) if swot_parts else "（未生成 SWOT）"

        # 波特五力
        porters_text = self._porters_to_report(state.porters) if state.porters else "（未生成波特五力分析）"

        # 战略建议
        rec_lines = []
        for r in state.recommendations:
            rec_lines.append(
                f"### {r.priority}. {r.title}\n"
                f"- **类别:** {r.category}\n"
                f"- **描述:** {r.description}\n"
                f"- **依据:** {r.rationale}\n"
                f"- **投入/影响/周期:** {r.effort} / {r.impact} / {r.timeline}\n"
            )
        recommendations_text = "\n".join(rec_lines) if rec_lines else "（未生成建议）"

        return {
            "competitor_profiles_text": competitor_profiles_text,
            "feature_matrix_text": feature_matrix_text,
            "swot_text": swot_text,
            "porters_text": porters_text,
            "business_model_text": state.business_model_analysis or "（未生成商业模式分析）",
            "ux_text": state.ux_comparison or "（未生成用户体验对比）",
            "tech_text": state.tech_comparison or "（未生成技术对比）",
            "positioning_text": state.competitive_positioning or "（未生成竞争定位）",
            "risk_text": state.risk_assessment or "（未生成风险评估）",
            "recommendations_text": recommendations_text,
        }

    async def _compile_report(self, state: AnalysisState, modules: dict) -> str:
        competitor_names = ", ".join(cp.name for cp in state.competitor_profiles)
        prompt = prompts.COMPILE_FULL_REPORT.format(
            our_product=state.request.our_product,
            date=datetime.now().strftime("%Y-%m-%d"),
            competitor_names=competitor_names,
            target_audience=state.request.target_audience,
            executive_summary=state.executive_summary,
            industry_context=state.industry_context,
            **modules,
        )
        return await chat_completion(
            prompts.SYSTEM_PROMPT, prompt, max_tokens=8192
        )

    def _export(self, state: AnalysisState) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = state.request.our_product.replace(" ", "_").replace("/", "_")
        filename = f"竞品分析_{safe_name}_{timestamp}.md"
        path = OUTPUT_DIR / filename
        path.write_text(state.final_report_md, encoding="utf-8")
        return path

    @staticmethod
    def _profile_to_report_section(cp) -> str:
        return (
            f"### {cp.name}\n"
            f"- **定位:** {cp.description}\n"
            f"- **竞品类型:** {cp.tier.value}\n"
            f"- **融资:** {cp.funding_stage}（累计 {cp.funding_total}）\n"
            f"- **规模:** {cp.employee_count}\n"
            f"- **核心产品:** {', '.join(cp.key_products)}\n"
            f"- **目标用户:** {cp.target_users}\n"
            f"- **定价:** {cp.pricing_model}\n"
            f"- **技术栈:** {', '.join(cp.tech_stack)}\n"
            f"- **优势:** {'; '.join(cp.strengths)}\n"
            f"- **劣势:** {'; '.join(cp.weaknesses)}\n"
            f"- **近期动态:** {'; '.join(cp.recent_moves)}\n"
        )

    @staticmethod
    def _porters_to_report(porters) -> str:
        if isinstance(porters, dict):
            lines = []
            labels = {
                "supplier_power": "供应商议价能力",
                "buyer_power": "买方议价能力",
                "competitive_rivalry": "行业竞争程度",
                "threat_of_substitution": "替代品威胁",
                "threat_of_new_entry": "新进入者威胁",
            }
            for key, label in labels.items():
                item = porters.get(key, {})
                if isinstance(item, dict):
                    lines.append(
                        f"**{label}:** {item.get('level', 'N/A')}\n"
                        f"{item.get('analysis', '')}\n"
                    )
                else:
                    lines.append(f"**{label}:** {item}\n")
            overall = porters.get("overall_assessment", "")
            if overall:
                lines.append(f"\n**综合评估:** {overall}")
            return "\n".join(lines)
        return str(porters)
