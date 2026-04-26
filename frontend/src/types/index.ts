export interface LLMConfig {
  provider: string;
  api_key: string;
  model: string;
  base_url: string;
  tavily_api_key: string;
  serper_api_key: string;
}

export interface AnalysisRequest {
  our_product: string;
  our_description: string;
  industry: string;
  competitors: string[];
  focus_areas: string[];
  depth: 'quick' | 'standard' | 'deep';
  target_audience: string;
  llm_config?: LLMConfig;
}

export interface CompetitorProfile {
  name: string;
  tier: 'direct' | 'indirect' | 'potential';
  website: string;
  description: string;
  founding_year: number | null;
  headquarters: string;
  funding_stage: string;
  funding_total: string;
  employee_count: string;
  key_products: string[];
  target_users: string;
  pricing_model: string;
  tech_stack: string[];
  strengths: string[];
  weaknesses: string[];
  recent_moves: string[];
}

export interface SWOTResult {
  company: string;
  strengths: string[];
  weaknesses: string[];
  opportunities: string[];
  threats: string[];
}

export interface FeatureComparison {
  feature_name: string;
  scores: Record<string, string>;
}

export interface StrategicRecommendation {
  priority: number;
  category: string;
  title: string;
  description: string;
  rationale: string;
  effort: string;
  impact: string;
  timeline: string;
}

export interface AnalysisState {
  created_at: string;
  our_profile: CompetitorProfile | null;
  competitor_profiles: CompetitorProfile[];
  industry_context: string;
  market_trends: string[];
  swot_results: SWOTResult[];
  porters: any;
  feature_matrix: FeatureComparison[];
  business_model_analysis: string;
  ux_comparison: string;
  tech_comparison: string;
  strategic_summary: string;
  recommendations: StrategicRecommendation[];
  competitive_positioning: string;
  risk_assessment: string;
  final_report_md: string;
  executive_summary: string;
  agent_logs: string[];
  errors: string[];
}

export interface ProgressEvent {
  stage_idx: number;
  total: number;
  status: 'running' | 'done' | 'error';
  message: string;
  elapsed: number;
}
