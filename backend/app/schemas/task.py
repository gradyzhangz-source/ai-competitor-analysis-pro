from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional, Any, Dict
from datetime import datetime

class LLMConfigOverride(BaseModel):
    provider: str = "openai"
    api_key: str = ""
    model: str = ""
    base_url: str = ""
    tavily_api_key: str = ""
    serper_api_key: str = ""

class TaskCreate(BaseModel):
    our_product: str
    our_description: str = ""
    industry: str = ""
    competitors: List[str] = Field(default_factory=list)
    focus_areas: List[str] = Field(default_factory=list)
    depth: str = "standard"
    target_audience: str = "产品团队"
    llm_config: Optional[LLMConfigOverride] = None

class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_name: str
    industry: str
    competitors: List[str]
    status: str
    created_at: datetime
    updated_at: datetime
    result_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
