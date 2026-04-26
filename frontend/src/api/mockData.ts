import { AnalysisRequest, AnalysisState, ProgressEvent } from '../types';

export const runStaticDemo = async (
  request: AnalysisRequest,
  onProgress: (data: ProgressEvent) => void,
  onResult: (data: AnalysisState) => void
) => {
  const stages = ['信息收集', '深度分析', '战略建议', '报告生成'];

  for (let i = 0; i < stages.length; i += 1) {
    onProgress({
      stage_idx: i,
      total: stages.length,
      status: 'running',
      message: `${stages[i]}进行中...`,
      elapsed: 0,
    });
    await new Promise((resolve) => setTimeout(resolve, 650));
    onProgress({
      stage_idx: i,
      total: stages.length,
      status: 'done',
      message: `${stages[i]}完成`,
      elapsed: 0.6,
    });
  }

  onResult(createMockAnalysisState(request));
};

export const createMockAnalysisState = (request: AnalysisRequest): AnalysisState => {
  const product = request.our_product || 'Cursor';
  const competitors = request.competitors.length
    ? request.competitors
    : ['GitHub Copilot', 'Windsurf', 'Cline'];
  const [first, second = 'Windsurf', third = 'Cline'] = competitors;

  return {
    created_at: new Date().toISOString(),
    our_profile: {
      name: product,
      tier: 'direct',
      website: '',
      description: `${product} 是面向知识工作者与产品团队的 AI 原生效率工具，强调自动化分析、结构化输出与可解释建议。`,
      founding_year: null,
      headquarters: '',
      funding_stage: '待验证',
      funding_total: '待验证',
      employee_count: '待验证',
      key_products: ['AI 工作流', '报告生成', '可视化分析看板'],
      target_users: '互联网产品经理、战略分析师、增长团队、创业团队',
      pricing_model: 'SaaS 订阅制 + 企业定制',
      tech_stack: ['React', 'FastAPI', 'Multi-Agent', 'LLM', 'SSE'],
      strengths: ['多 Agent 分工清晰', '报告结构化程度高', '适合 PM 高频分析场景'],
      weaknesses: ['实时数据质量依赖外部搜索 API', '深度行业知识仍需人工复核'],
      recent_moves: ['新增 GitHub Pages 静态演示模式', '支持报告在线编辑与 PDF 导出'],
    },
    competitor_profiles: competitors.map((name, index) => ({
      name,
      tier: index === 0 ? 'direct' : index === 1 ? 'indirect' : 'potential',
      website: '',
      description:
        index === 0
          ? `${name} 具备强品牌认知和生态入口优势，是直接竞争标杆。`
          : `${name} 在垂直场景、用户体验或自动化能力上形成差异化竞争。`,
      founding_year: null,
      headquarters: '待验证',
      funding_stage: '待验证',
      funding_total: '待验证',
      employee_count: '待验证',
      key_products: ['AI 辅助分析', '协作工作台', '自动化能力'],
      target_users: '专业用户、企业团队、效率工具用户',
      pricing_model: '免费增值 / 订阅制',
      tech_stack: ['LLM', '云端服务', '插件生态'],
      strengths:
        index === 0
          ? ['品牌心智强', '生态资源丰富', '用户获取成本低']
          : ['垂直场景聚焦', '体验迭代快', '差异化能力明显'],
      weaknesses:
        index === 0
          ? ['定制化深度有限', '跨框架商业分析能力不足']
          : ['品牌影响力较弱', '企业级能力仍需验证'],
      recent_moves: ['持续增强 AI 工作流能力', '加强企业级场景覆盖'],
    })),
    industry_context:
      'AI 产品经理工具正在从“单点提效”进入“工作流自动化”阶段。竞品分析、用户研究、PRD 生成、数据解读等高频 PM 工作具备明显的结构化和可自动化特征。行业关键竞争点正在从单纯模型能力转向场景理解、工作流编排、输出可信度和团队协作能力。',
    market_trends: ['Multi-Agent 工作流产品化', 'AI 报告可视化', '企业级权限与审计', '人机协同编辑'],
    swot_results: [
      {
        company: product,
        strengths: ['Agent 架构清晰，适合复杂任务拆解', '输出包含图表、报告、建议，完整度高', '可作为 PM 作品集展示工程化能力'],
        weaknesses: ['线上真实分析需部署后端 API', '行业事实仍需人工校验', '对长文本和搜索质量有依赖'],
        opportunities: ['AI PM 工具市场快速增长', '企业对自动化研究报告需求强', '可扩展到用户研究、需求分析、投融资分析'],
        threats: ['通用大模型持续增强', '竞品可能内置类似模板', '数据源合规与准确性风险'],
      },
      {
        company: first,
        strengths: ['品牌优势明显', '生态入口强', '用户认知成本低'],
        weaknesses: ['专用竞品分析能力不足', '报告可编辑与可视化能力有限'],
        opportunities: ['可通过插件扩展 PM 场景', '企业客户付费意愿较强'],
        threats: ['垂直 PM Agent 形成差异化', '用户对结构化输出要求提高'],
      },
    ],
    porters: {
      supplier_power: { level: '中', analysis: '底层模型和搜索 API 是关键供应方，但可通过多模型适配降低依赖。' },
      buyer_power: { level: '高', analysis: 'PM 和企业团队工具选择多，要求低学习成本、强输出质量和可验证价值。' },
      competitive_rivalry: { level: '高', analysis: 'AI 效率工具竞争激烈，核心差异在于场景深度和工作流闭环。' },
      threat_of_substitution: { level: '中', analysis: '通用 ChatGPT/Claude 可替代部分能力，但难以替代完整 SaaS 工作流。' },
      threat_of_new_entry: { level: '中', analysis: '技术门槛下降，但高质量产品体验和业务框架积累仍是壁垒。' },
      overall_assessment: '该赛道竞争强度高，但垂直 PM 场景仍有差异化空间。产品应优先强化可视化、可编辑、可导出的工作流闭环。',
    },
    feature_matrix: [
      { feature_name: '[核心能力] Multi-Agent 工作流', scores: { [product]: '★★★★★ 完整四阶段流水线', [first]: '★★★ 依赖通用对话', [second]: '★★★ 场景能力较强', [third]: '★★ 垂直度有限' } },
      { feature_name: '[报告能力] SWOT / 五力 / 功能矩阵', scores: { [product]: '★★★★★ 内置商业框架', [first]: '★★ 需手动提示', [second]: '★★★ 有部分模板', [third]: '★★ 结构化不足' } },
      { feature_name: '[体验] 实时进度与可观测性', scores: { [product]: '★★★★ SSE 进度透出', [first]: '★★★ 基础流式', [second]: '★★★ 交互较顺滑', [third]: '★★ 反馈不足' } },
      { feature_name: '[流转] 在线编辑与 PDF 导出', scores: { [product]: '★★★★★ 支持编辑和导出', [first]: '★★ 需外部工具', [second]: '★★★ 部分支持', [third]: '★★ 不完整' } },
    ],
    business_model_analysis:
      '建议采用 Freemium + Pro 订阅 + 企业版三层模式。个人用户可免费生成基础报告，Pro 用户获得深度分析、历史记录和导出能力，企业版提供私有化部署、数据源接入和权限管理。',
    ux_comparison:
      '该产品相比通用大模型的核心 UX 差异在于：用户无需组织复杂提示词，只需要输入产品、行业和竞品，即可获得结构化、可编辑、可导出的分析结果。',
    tech_comparison:
      '技术上采用 React + FastAPI + SQLite + Multi-Agent 架构，兼顾演示体验、工程可读性和后续云部署扩展能力。静态模式可独立展示，API 模式可接入真实 LLM。',
    strategic_summary:
      '优先将产品定位为“AI 产品经理的自动化竞品研究工作台”，避免与通用 Chatbot 正面对抗，强化专业框架、可视化和协作流转能力。',
    recommendations: [
      {
        priority: 1,
        category: 'product',
        title: '强化静态演示闭环',
        description: '保证 GitHub Pages 无后端时也能完整演示核心价值，降低面试展示风险。',
        rationale: '作品集项目的第一目标是可访问、可理解、可演示。',
        effort: 'low',
        impact: 'high',
        timeline: 'short',
      },
      {
        priority: 2,
        category: 'technology',
        title: '部署云端 API',
        description: '将 FastAPI 部署到 Railway/Render，并通过 VITE_API_BASE 接入 GitHub Pages。',
        rationale: '静态站负责展示，云端 API 负责真实分析，形成完整产品闭环。',
        effort: 'medium',
        impact: 'high',
        timeline: 'medium',
      },
      {
        priority: 3,
        category: 'marketing',
        title: '补充案例截图',
        description: '在 README 中增加页面截图、报告样例和面试讲解话术，提高 GitHub 转化效果。',
        rationale: '招聘场景下，截图和结果样例比代码目录更容易让面试官快速理解价值。',
        effort: 'low',
        impact: 'medium',
        timeline: 'short',
      },
    ],
    competitive_positioning:
      `建议将 ${product} 定位为“面向 AI 产品经理与战略团队的自动化竞品分析工作台”。核心差异化不是单次问答，而是从输入、分析、可视化、编辑到导出的完整工作流。`,
    risk_assessment:
      '主要风险包括：真实数据来源不稳定、模型输出需要人工复核、纯静态页面无法运行后端。应通过静态演示模式、云端 API 部署和免责声明降低演示与使用风险。',
    final_report_md: `# ${product} 竞品分析报告\n\n## Executive Summary\n${product} 适合定位为面向 AI 产品经理的自动化竞品分析平台。它通过 Multi-Agent 工作流，把传统 1-2 天的竞品研究压缩为数分钟，并输出可视化、可编辑、可导出的商业报告。\n\n## 核心竞争判断\n- 与通用 Chatbot 相比，优势在于场景化工作流和结构化商业框架。\n- 与传统文档工具相比，优势在于自动完成信息抽取、对比分析和战略建议生成。\n- GitHub Pages 静态模式可作为作品集演示入口，云端 API 模式可作为真实产品落地形态。\n\n## 建议\n1. 保持 GitHub Pages 纯静态可访问，确保面试展示稳定。\n2. 后续将 FastAPI 部署到 Railway/Render，形成真实在线分析能力。\n3. 在 README 增加截图、架构图、案例报告和简历描述。\n`,
    executive_summary:
      `${product} 是一个面向 AI 产品经理作品集展示的竞品分析平台。其核心亮点在于 Multi-Agent 任务拆解、商业分析框架结构化、图表可视化、在线编辑与 PDF 导出。静态模式确保 GitHub Pages 无后端也可完整演示，适合面试现场展示。`,
    agent_logs: [
      '[StaticDemo] GitHub Pages 静态演示模式启动',
      '[ResearchAgent] 模拟完成竞品画像构建',
      '[AnalysisAgent] 模拟完成 SWOT / 五力 / 功能矩阵',
      '[StrategyAgent] 模拟完成竞争定位与行动建议',
      '[ReportAgent] 模拟完成 Markdown 报告生成',
    ],
    errors: [],
  };
};
