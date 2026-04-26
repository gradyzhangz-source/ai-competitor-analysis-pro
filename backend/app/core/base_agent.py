"""
Agent 基类 — 统一接口、生命周期管理、日志
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from app.schemas.analysis import AnalysisState


class BaseAgent(ABC):
    """所有 Agent 的基类"""

    name: str = "BaseAgent"

    @abstractmethod
    async def run(self, state: AnalysisState) -> AnalysisState:
        """执行 Agent 任务，读取并更新共享 state"""
        ...

    def log(self, state: AnalysisState, msg: str):
        state.log(self.name, msg)
        print(f"  [{self.name}] {msg}")
