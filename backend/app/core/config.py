"""
竞品分析 Agent 系统 — 全局配置
"""
import os
from pathlib import Path

# ── 路径 ──
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# ── LLM 配置 ──
# 支持 OpenAI / DeepSeek / 任何 OpenAI-compatible API
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # openai | deepseek | custom

LLM_CONFIG = {
    "openai": {
        "api_key": os.getenv("OPENAI_API_KEY", ""),
        "base_url": "https://api.openai.com/v1",
        "model": os.getenv("OPENAI_MODEL", "gpt-4o"),
    },
    "deepseek": {
        "api_key": os.getenv("DEEPSEEK_API_KEY", ""),
        "base_url": "https://api.deepseek.com/v1",
        "model": os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
    },
    "custom": {
        "api_key": os.getenv("CUSTOM_API_KEY", ""),
        "base_url": os.getenv("CUSTOM_BASE_URL", "http://localhost:8000/v1"),
        "model": os.getenv("CUSTOM_MODEL", "default"),
    },
}

def get_llm_config() -> dict:
    return LLM_CONFIG[LLM_PROVIDER]

# ── 搜索工具配置 ──
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")

# ── Agent 参数 ──
MAX_RETRIES = 3
REQUEST_TIMEOUT = 120
TEMPERATURE = 0.3
MAX_TOKENS = 4096
SEARCH_RESULTS_PER_QUERY = 8

# ── 分析框架开关 ──
ENABLED_FRAMEWORKS = [
    "product_comparison",   # 产品功能对比矩阵
    "swot",                 # SWOT 分析
    "porters_five_forces",  # 波特五力
    "business_model",       # 商业模式画布
    "user_experience",      # 用户体验对比
    "technology_stack",     # 技术架构分析
]
