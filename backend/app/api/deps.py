import contextlib
from app.core import config
from app.utils.llm_client import reset_client
from app.schemas.task import LLMConfigOverride
from app.core.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextlib.contextmanager
def override_config(override: LLMConfigOverride):
    if not override:
        yield
        return

    # Save old
    old_provider = config.LLM_PROVIDER
    old_tavily = config.TAVILY_API_KEY
    old_serper = config.SERPER_API_KEY
    
    provider = override.provider
    old_llm_cfg = {}
    if provider in config.LLM_CONFIG:
        old_llm_cfg = config.LLM_CONFIG[provider].copy()

    # Apply new
    config.LLM_PROVIDER = provider
    if provider in config.LLM_CONFIG:
        if override.api_key:
            config.LLM_CONFIG[provider]["api_key"] = override.api_key
        if override.model:
            config.LLM_CONFIG[provider]["model"] = override.model
        if override.base_url:
            config.LLM_CONFIG[provider]["base_url"] = override.base_url

    if override.tavily_api_key:
        config.TAVILY_API_KEY = override.tavily_api_key
    if override.serper_api_key:
        config.SERPER_API_KEY = override.serper_api_key

    reset_client()

    try:
        yield
    finally:
        # Restore
        config.LLM_PROVIDER = old_provider
        config.TAVILY_API_KEY = old_tavily
        config.SERPER_API_KEY = old_serper
        if provider in config.LLM_CONFIG:
            config.LLM_CONFIG[provider].update(old_llm_cfg)
        reset_client()
