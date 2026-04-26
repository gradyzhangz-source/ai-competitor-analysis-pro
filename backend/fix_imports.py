import os
from pathlib import Path

backend_dir = Path("/Users/wangcaitian/Desktop/project1/ai-competitor-analysis-pro/backend/app")

replacements = [
    ("from core.base_agent", "from app.core.base_agent"),
    ("from models.schemas", "from app.schemas.analysis"),
    ("from tools.llm_client", "from app.utils.llm_client"),
    ("from tools.web_search", "from app.utils.web_search"),
    ("from tools.data_processor", "from app.utils.data_processor"),
    ("from prompts import", "from app.prompts import"),
    ("import config", "from app.core import config"),
    ("from config import", "from app.core.config import"),
    ("from agents.", "from app.agents."),
]

for root, dirs, files in os.walk(backend_dir):
    for file in files:
        if file.endswith(".py"):
            filepath = os.path.join(root, file)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            new_content = content
            for old, new in replacements:
                new_content = new_content.replace(old, new)
            
            if new_content != content:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Fixed imports in {filepath}")
