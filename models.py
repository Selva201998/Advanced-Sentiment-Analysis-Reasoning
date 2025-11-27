
from dataclasses import dataclass, field
from typing import Any, Dict, List
import time

@dataclass
class Message:
    role: str
    content: str

@dataclass
class TraceStep:
    step_name: str
    input: Dict[str, Any]
    output: Dict[str, Any]
    timestamp: float = field(default_factory=lambda: time.time())

@dataclass
class ReasoningTrace:
    request_id: str
    steps: List[TraceStep] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_step(self, step_name: str, input: Dict[str, Any], output: Dict[str, Any]):
        self.steps.append(TraceStep(step_name=step_name, input=input, output=output))
