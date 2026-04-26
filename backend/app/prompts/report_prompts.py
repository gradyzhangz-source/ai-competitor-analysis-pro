"""
Report Agent 提示词 — 报告生成与排版
"""

SYSTEM_PROMPT = """\
你是一名专业的商业分析报告撰写者，擅长将复杂的分析数据和洞察整合为
结构清晰、逻辑严密、适合高管阅读的分析报告。

## 写作原则
1. 开头必须有 Executive Summary，30 秒内传递核心结论
2. 结构层次分明，善用标题、表格、列表
3. 数据和观点结合，不堆砌信息
4. 结尾必须有明确的行动建议
5. 语言专业简洁，避免冗余
"""

EXECUTIVE_SUMMARY = """\
请基于以下完整分析内容，撰写一份 Executive Summary（高管摘要）。

## 分析概况
- 我方产品：{our_product}
- 行业：{industry}
- 竞品数量：{competitor_count}
- 分析深度：{depth}

## 关键发现摘要
{key_findings}

## 输出要求
- 150-250 字
- 必须包含：1）竞争格局结论  2）我方位置判断  3）最关键的 3 条建议
- 语气：自信、专业、直接
- 适合不看完整报告的高管快速获取核心信息
"""

COMPILE_FULL_REPORT = """\
请将以下所有分析模块整合为一份完整的竞品分析报告。

## 报告元数据
- 标题：{our_product} 竞品分析报告
- 日期：{date}
- 分析对象：{competitor_names}
- 报告受众：{target_audience}

## 各模块内容

### Executive Summary
{executive_summary}

### 行业背景
{industry_context}

### 竞品画像
{competitor_profiles_text}

### 产品功能对比
{feature_matrix_text}

### SWOT 分析
{swot_text}

### 波特五力分析
{porters_text}

### 商业模式对比
{business_model_text}

### 用户体验对比
{ux_text}

### 技术对比
{tech_text}

### 竞争定位
{positioning_text}

### 风险评估
{risk_text}

### 战略建议
{recommendations_text}

---

## 整合要求
1. 保持上述所有模块内容完整，合理调整排版和过渡语
2. 添加目录结构
3. 统一编号体系
4. 确保报告开头是 Executive Summary
5. 确保报告结尾是"行动建议"和"下一步"
6. 添加适当的过渡段落，使报告阅读体验流畅
7. 如有重复内容，进行合并精简
8. 在报告末尾添加免责声明："本报告基于公开信息和 AI 分析生成，仅供参考，
   不构成商业决策依据。关键判断建议结合内部数据和专家意见进一步验证。"

输出完整 Markdown 格式报告。
"""
