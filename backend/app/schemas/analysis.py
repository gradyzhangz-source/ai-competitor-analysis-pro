"""
数据模型定义 — 贯穿整个分析流水线的结构化数据类型
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class AnalysisDepth(str, Enum):
    QUICK = "quick"          # 5 分钟快速扫描
    STANDARD = "standard"    # 标准分析
    DEEP = "deep"            # 深度研究


class CompetitorTier(str, Enum):
    DIRECT = "direct"        # 直接竞品
    INDIRECT = "indirect"    # 间接竞品
    POTENTIAL = "potential"  # 潜在竞品


@dataclass
class CompetitorProfile:
    name: str
    tier: CompetitorTier = CompetitorTier.DIRECT
    website: str = ""
    description: str = ""
    founding_year: Optional[int] = None
    headquarters: str = ""
    funding_stage: str = ""
    funding_total: str = ""
    employee_count: str = ""
    key_products: list[str] = field(default_factory=list)
    target_users: str = ""
    pricing_model: str = ""
    tech_stack: list[str] = field(default_factory=list)
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    recent_moves: list[str] = field(default_factory=list)
    raw_search_data: list[str] = field(default_factory=list)


@dataclass
class SWOTResult:
    company: str
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    opportunities: list[str] = field(default_factory=list)
    threats: list[str] = field(default_factory=list)


@dataclass
class PortersFiveForces:
    supplier_power: str = ""
    buyer_power: str = ""
    competitive_rivalry: str = ""
    threat_of_substitution: str = ""
    threat_of_new_entry: str = ""
    overall_assessment: str = ""


@dataclass
class FeatureComparison:
    feature_name: str
    scores: dict[str, str] = field(default_factory=dict)  # company -> rating/description


@dataclass
class StrategicRecommendation:
    priority: int  # 1 = highest
    category: str  # product / marketing / technology / partnership
    title: str = ""
    description: str = ""
    rationale: str = ""
    effort: str = ""     # low / medium / high
    impact: str = ""     # low / medium / high
    timeline: str = ""   # short / medium / long term


@dataclass
class AnalysisRequest:
    """用户输入 — 分析任务定义"""
    our_product: str
    our_description: str = ""
    competitors: list[str] = field(default_factory=list)
    industry: str = ""
    focus_areas: list[str] = field(default_factory=list)
    depth: AnalysisDepth = AnalysisDepth.STANDARD
    target_audience: str = "产品团队"  # 报告读者


@dataclass
class AnalysisState:
    """Agent 之间共享的全局状态"""
    request: AnalysisRequest
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    # Research Agent 输出
    our_profile: Optional[CompetitorProfile] = None
    competitor_profiles: list[CompetitorProfile] = field(default_factory=list)
    industry_context: str = ""
    market_trends: list[str] = field(default_factory=list)

    # Analysis Agent 输出
    swot_results: list[SWOTResult] = field(default_factory=list)
    porters: Optional[PortersFiveForces] = None
    feature_matrix: list[FeatureComparison] = field(default_factory=list)
    business_model_analysis: str = ""
    ux_comparison: str = ""
    tech_comparison: str = ""

    # Strategy Agent 输出
    strategic_summary: str = ""
    recommendations: list[StrategicRecommendation] = field(default_factory=list)
    competitive_positioning: str = ""
    risk_assessment: str = ""

    # Report Agent 输出
    final_report_md: str = ""
    executive_summary: str = ""

    # 元数据
    agent_logs: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def log(self, agent: str, message: str):
        entry = f"[{datetime.now().strftime('%H:%M:%S')}] [{agent}] {message}"
        self.agent_logs.append(entry)
