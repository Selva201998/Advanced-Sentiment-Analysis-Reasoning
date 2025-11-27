
from typing import Dict
import hashlib

class MockAdapter:
    """A deterministic mock LLM adapter. It hashes prompt text to create repeatable outputs."""
    def __init__(self, name: str = "mock", deterministic: bool = True):
        self.name = name
        self.deterministic = deterministic

    def generate(self, prompt: str, max_tokens: int = 256) -> Dict[str, object]:
        # Deterministic pseudo-response based on prompt content
        h = hashlib.sha256(prompt.encode('utf-8')).hexdigest()
        # simple deterministic 'classification' example
        cls = "positive" if int(h[:2], 16) % 2 == 0 else "negative"
        confidence = (int(h[-2:], 16) % 100) / 100.0
        return {"text": f"Classification: {cls}", "classification": cls, "confidence": confidence}
