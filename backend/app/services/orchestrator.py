"""
Orchestrator — 核心编排器
职责：按 DAG 依赖顺序调度 4 个 Agent，管理全局状态，错误恢复
面试讲解重点：流水线设计、状态机、容错策略、可观测性
"""
from __future__ import annotations
import asyncio
import time
from datetime import datetime
from typing import Callable, Optional

from app.core.base_agent import BaseAgent
from app.schemas.analysis import AnalysisState, AnalysisRequest
from app.agents.research_agent import ResearchAgent
from app.agents.analysis_agent import AnalysisAgent
from app.agents.strategy_agent import StrategyAgent
from app.agents.report_agent import ReportAgent

# Agent 阶段元信息，供 UI 展示
PIPELINE_STAGES = [
    {"name": "ResearchAgent",  "label": "信息收集",  "icon": "🔍", "desc": "搜索竞品信息，构建画像"},
    {"name": "AnalysisAgent",  "label": "深度分析",  "icon": "📊", "desc": "SWOT / 五力 / 功能矩阵"},
    {"name": "StrategyAgent",  "label": "战略建议",  "icon": "🎯", "desc": "竞争定位与行动建议"},
    {"name": "ReportAgent",    "label": "报告生成",  "icon": "📄", "desc": "整合输出完整报告"},
]


class Orchestrator:
    """
    Agent 流水线编排器

    执行顺序（线性 DAG）:
    ResearchAgent → AnalysisAgent → StrategyAgent → ReportAgent

    每个 Agent 读取并更新共享的 AnalysisState。
    支持可选的 progress_callback 用于 Web UI 实时更新。
    """

    def __init__(self):
        self.pipeline: list[BaseAgent] = [
            ResearchAgent(),
            AnalysisAgent(),
            StrategyAgent(),
            ReportAgent(),
        ]

    async def run(
        self,
        request: AnalysisRequest,
        progress_callback: Optional[Callable] = None,
    ) -> AnalysisState:
        state = AnalysisState(request=request)
        state.log("Orchestrator", "=" * 50)
        state.log("Orchestrator", f"竞品分析任务启动")
        state.log("Orchestrator", f"产品: {request.our_product}")
        state.log("Orchestrator", f"竞品: {', '.join(request.competitors)}")
        state.log("Orchestrator", f"深度: {request.depth.value}")
        state.log("Orchestrator", "=" * 50)

        def _notify(stage_idx: int, status: str, message: str = "", elapsed: float = 0):
            """统一通知：同时写日志 + 回调 UI"""
            if message:
                state.log("Orchestrator", message)
            print(f"  [{status}] Stage {stage_idx + 1}: {message}")
            if progress_callback:
                progress_callback(stage_idx, len(self.pipeline), status, message, elapsed)

        total_start = time.time()

        for i, agent in enumerate(self.pipeline):
            step_start = time.time()
            stage = PIPELINE_STAGES[i]
            header = f"[Stage {i+1}/{len(self.pipeline)}] {stage['icon']} {stage['label']}"
            print(f"\n{'='*60}")
            print(f"  {header}")
            print(f"{'='*60}")

            _notify(i, "running", f"{stage['label']}进行中...")

            try:
                state = await agent.run(state)
                elapsed = time.time() - step_start
                _notify(i, "done", f"{stage['label']}完成 ({elapsed:.1f}s)", elapsed)
            except Exception as e:
                elapsed = time.time() - step_start
                error_msg = f"{agent.name} 失败 ({elapsed:.1f}s): {e}"
                state.errors.append(error_msg)
                _notify(i, "error", error_msg, elapsed)
                if isinstance(agent, ResearchAgent):
                    break
                continue

        total_elapsed = time.time() - total_start
        state.log("Orchestrator", f"全部完成，总耗时 {total_elapsed:.1f}s")

        print(f"\n{'='*60}")
        print(f"  分析完成！总耗时: {total_elapsed:.1f}s")
        if state.errors:
            print(f"  ⚠ {len(state.errors)} 个错误:")
            for err in state.errors:
                print(f"    - {err}")
        print(f"{'='*60}\n")

        return state
