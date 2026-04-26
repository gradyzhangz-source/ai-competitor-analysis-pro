"""
Analysis Agent 提示词 — 多框架深度分析
"""

SYSTEM_PROMPT = """\
你是一名资深的战略分析师，精通 Porter's Five Forces、SWOT、商业模式画布等主流分析框架。
你的分析风格严谨、结构化、数据驱动，善于从竞品信息中洞察深层竞争逻辑。

## 工作原则
1. 每个分析维度必须给出具体证据或推理依据
2. 避免泛泛而谈，要有 actionable insight
3. 对比分析时要公正客观，不刻意贬低竞品
4. 不确定的判断要标注置信度
"""

PRODUCT_FEATURE_MATRIX = """\
请基于以下竞品画像，生成产品功能对比矩阵。

## 我方产品
{our_profile}

## 竞品画像
{competitor_profiles}

## 行业与关注领域
- 行业：{industry}
- 重点关注：{focus_areas}

## 输出要求
请输出 JSON 格式的功能对比矩阵：
{{
  "dimensions": [
    {{
      "category": "功能大类（如：核心功能/用户体验/数据能力/生态集成/定价）",
      "features": [
        {{
          "feature_name": "具体功能点",
          "scores": {{
            "公司A": "⭐⭐⭐⭐⭐ 简评",
            "公司B": "⭐⭐⭐ 简评"
          }}
        }}
      ]
    }}
  ],
  "summary": "整体对比结论（2-3句）"
}}

要求：
- 至少覆盖 5 个维度，每个维度 3-5 个功能点
- 评分用⭐表示（1-5星），必须附带简短说明
- 必须包含定价对比维度
"""

SWOT_ANALYSIS = """\
请对以下公司进行 SWOT 分析。

## 公司信息
{company_profile}

## 行业背景
{industry_context}

## 竞争对手信息（用于相对判断）
{competitor_summary}

## 输出要求
严格输出以下 JSON 格式：
{{
  "company": "{company_name}",
  "strengths": [
    "S1: 具体优势描述（附证据/推理）",
    "S2: ..."
  ],
  "weaknesses": [
    "W1: 具体劣势描述（附证据/推理）",
    "W2: ..."
  ],
  "opportunities": [
    "O1: 市场机会描述",
    "O2: ..."
  ],
  "threats": [
    "T1: 外部威胁描述",
    "T2: ..."
  ]
}}

要求：
- 每个维度至少 3 条，最多 5 条
- Strengths/Weaknesses 聚焦内部能力
- Opportunities/Threats 聚焦外部环境
- 每条必须具体，不要写"产品不够完善"这种空话
"""

PORTERS_FIVE_FORCES = """\
请对 **{industry}** 行业进行波特五力分析。

## 行业背景
{industry_context}

## 主要玩家信息
{all_profiles_summary}

## 输出要求
请输出 JSON：
{{
  "supplier_power": {{
    "level": "高/中/低",
    "analysis": "分析说明（100-150字）",
    "key_factors": ["因素1", "因素2"]
  }},
  "buyer_power": {{
    "level": "高/中/低",
    "analysis": "",
    "key_factors": []
  }},
  "competitive_rivalry": {{
    "level": "高/中/低",
    "analysis": "",
    "key_factors": []
  }},
  "threat_of_substitution": {{
    "level": "高/中/低",
    "analysis": "",
    "key_factors": []
  }},
  "threat_of_new_entry": {{
    "level": "高/中/低",
    "analysis": "",
    "key_factors": []
  }},
  "overall_assessment": "综合判断行业竞争强度与吸引力（100字）"
}}
"""

BUSINESS_MODEL_COMPARISON = """\
请对比分析以下公司的商业模式。

## 公司画像
{all_profiles}

## 输出要求
使用商业模式画布（Business Model Canvas）的 9 个维度进行对比：
1. 客户细分 (Customer Segments)
2. 价值主张 (Value Propositions)
3. 渠道通路 (Channels)
4. 客户关系 (Customer Relationships)
5. 收入来源 (Revenue Streams)
6. 核心资源 (Key Resources)
7. 关键业务 (Key Activities)
8. 重要合作 (Key Partnerships)
9. 成本结构 (Cost Structure)

对每个维度，用表格形式对比所有公司，然后给出 1-2 句洞察。
输出 Markdown 格式，300-500 字。
"""

UX_COMPARISON = """\
请从用户体验角度对比分析以下产品。

## 产品信息
{all_profiles}

## 对比维度
1. 核心使用场景与用户旅程
2. 上手门槛与学习曲线
3. 界面设计理念
4. 核心交互差异点
5. 用户口碑与满意度信号

输出 Markdown 格式，200-400 字，重点突出差异化。
"""

TECH_COMPARISON = """\
请从技术架构角度对比分析以下产品。

## 产品信息
{all_profiles}

## 对比维度
1. 核心技术栈
2. AI/算法能力
3. 数据处理能力
4. 开放性与可扩展性（API、插件生态）
5. 技术壁垒评估

输出 Markdown 格式，200-400 字。
"""
