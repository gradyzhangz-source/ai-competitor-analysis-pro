"""
Research Agent 提示词 — 信息收集与竞品画像构建
"""

SYSTEM_PROMPT = """\
你是一名顶尖的市场研究分析师，擅长高效收集和整理竞争对手情报。

## 核心能力
- 从碎片化信息中提炼结构化竞品画像
- 区分直接竞品、间接竞品、潜在竞品
- 识别市场趋势和行业动态

## 工作原则
1. 信息必须有据可依，不编造具体数据（营收、用户量等）
2. 如果信息不确定，明确标注"待验证"
3. 优先关注：产品能力、商业模式、融资动态、近期战略动作
4. 输出必须结构化，便于下游 Agent 消费
"""

GENERATE_SEARCH_QUERIES = """\
你需要对以下竞品进行全面的信息收集。请生成高质量的搜索查询词。

## 我方产品
- 名称：{our_product}
- 描述：{our_description}
- 行业：{industry}

## 需要调研的竞品列表
{competitor_list}

## 任务
为每个竞品生成 3-4 个搜索查询，覆盖以下维度：
1. 公司基本面（融资、团队、规模）
2. 产品能力与功能特性
3. 商业模式与定价策略
4. 近期动态（新产品发布、战略合作、用户反馈）

同时为行业整体生成 2 个宏观搜索查询。

请严格按以下 JSON 格式输出：
{{
  "competitor_queries": {{
    "竞品名称": ["查询1", "查询2", "查询3"]
  }},
  "industry_queries": ["行业查询1", "行业查询2"]
}}
"""

BUILD_COMPETITOR_PROFILE = """\
请根据以下搜索结果，为竞品 **{competitor_name}** 构建结构化画像。

## 搜索结果
{search_results}

## 上下文
- 我方产品：{our_product}（{our_description}）
- 行业：{industry}

## 输出要求
请严格输出以下 JSON 格式（值为空时填 ""）：
{{
  "name": "{competitor_name}",
  "tier": "direct/indirect/potential",
  "website": "",
  "description": "一句话定位",
  "founding_year": null,
  "headquarters": "",
  "funding_stage": "如：B轮 / 已上市",
  "funding_total": "如：5000万美元",
  "employee_count": "如：200-500人",
  "key_products": ["产品1", "产品2"],
  "target_users": "目标用户群体",
  "pricing_model": "定价模式描述",
  "tech_stack": ["技术1", "技术2"],
  "strengths": ["优势1", "优势2", "优势3"],
  "weaknesses": ["劣势1", "劣势2"],
  "recent_moves": ["近期动态1", "近期动态2"]
}}
"""

BUILD_OUR_PROFILE = """\
请根据以下信息，为我方产品构建结构化画像。

## 产品信息
- 名称：{our_product}
- 描述：{our_description}
- 行业：{industry}

## 补充搜索结果
{search_results}

## 输出要求
请以与竞品相同的 JSON 格式输出我方产品画像，特别注意：
- 客观描述优势和劣势
- 劣势部分是后续制定战略的关键输入，不要回避
{{
  "name": "{our_product}",
  "tier": "self",
  "website": "",
  "description": "",
  "founding_year": null,
  "headquarters": "",
  "funding_stage": "",
  "funding_total": "",
  "employee_count": "",
  "key_products": [],
  "target_users": "",
  "pricing_model": "",
  "tech_stack": [],
  "strengths": [],
  "weaknesses": [],
  "recent_moves": []
}}
"""

INDUSTRY_CONTEXT = """\
请基于以下搜索结果，撰写一段 {industry} 行业的宏观环境分析。

## 搜索结果
{search_results}

## 输出要求
请覆盖：
1. 行业发展阶段与市场规模趋势
2. 关键驱动因素
3. 监管与政策环境
4. 技术趋势
5. 3-5 个近期值得关注的行业事件/趋势

输出纯文本，Markdown 格式，300-500 字。
"""
