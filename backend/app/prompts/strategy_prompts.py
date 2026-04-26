"""
Strategy Agent 提示词 — 战略建议与定位
"""

SYSTEM_PROMPT = """\
你是一名资深的产品战略顾问，服务过多家科技公司的竞争策略制定。
你擅长将分析洞察转化为可落地的战略建议，按优先级排列，并评估投入产出比。

## 工作原则
1. 建议必须具体可执行，避免"加强创新"这类空话
2. 每条建议必须有明确的逻辑链：洞察→机会→行动→预期效果
3. 必须考虑资源约束，按投入产出比排序
4. 同时考虑攻（扩张）与守（防御）策略
"""

COMPETITIVE_POSITIONING = """\
请基于以下分析结果，为我方产品制定竞争定位策略。

## 我方产品
{our_profile}

## 竞品概况
{competitor_summary}

## SWOT 分析结果
{swot_results}

## 功能对比结论
{feature_matrix_summary}

## 输出要求
请输出：
1. **当前竞争位置判断**（领先/跟随/差异化/细分龙头）
2. **建议定位方向**（正面对抗/差异化/细分深耕/平台化）
3. **核心差异化要素**（3-5 个我方应强化的独特价值点）
4. **定位声明**（一句话品牌定位，如"面向___的___解决方案"）
5. **竞争策略选择**及理由

输出 Markdown 格式，300-500 字。
"""

STRATEGIC_RECOMMENDATIONS = """\
请基于以下完整分析，生成战略行动建议。

## 我方产品画像
{our_profile}

## 行业背景
{industry_context}

## 波特五力分析
{porters_summary}

## SWOT 分析
{swot_results}

## 竞争定位
{positioning}

## 功能差距
{feature_gaps}

## 报告受众
{target_audience}

## 输出要求
请生成 8-12 条战略建议，严格使用以下 JSON 格式：
{{
  "recommendations": [
    {{
      "priority": 1,
      "category": "product / marketing / technology / partnership / operations",
      "title": "建议标题（动词开头，10字以内）",
      "description": "具体行动描述（50-100字）",
      "rationale": "为什么要做这个（基于上述哪条分析洞察）",
      "effort": "low / medium / high",
      "impact": "low / medium / high",
      "timeline": "short(0-3月) / medium(3-6月) / long(6-12月)"
    }}
  ]
}}

排序规则：
- 优先：high impact + low effort（Quick Win）
- 其次：high impact + medium effort
- 最后：long-term strategic bet
"""

RISK_ASSESSMENT = """\
请基于以下竞争分析，输出风险评估。

## 完整分析背景
{analysis_summary}

## 输出要求
请从以下维度评估风险：

1. **竞品威胁风险**（哪个竞品最可能在哪个维度超越我们）
2. **市场变化风险**（行业趋势中哪些可能对我们不利）
3. **技术颠覆风险**（是否有新技术可能重新定义赛道）
4. **人才/资源风险**
5. **政策/合规风险**

每条风险给出：
- 发生概率（高/中/低）
- 影响程度（高/中/低）
- 建议应对措施

输出 Markdown 格式。
"""
