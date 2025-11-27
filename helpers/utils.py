
from typing import Dict, Any
import json
from pydantic import BaseModel, ValidationError

def sanitize_text(text: str) -> str:
    return " ".join(text.strip().split())

def to_json_safe(obj: Dict[str, Any]) -> str:
    try:
        return json.dumps(obj, ensure_ascii=False)
    except Exception:
        return str(obj)

class OutputSchema(BaseModel):
    classification: str
    confidence: float
    text: str = ""
