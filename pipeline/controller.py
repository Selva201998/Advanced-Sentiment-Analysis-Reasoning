
from adapters.mock_adapter import MockAdapter
from helpers.utils import sanitize_text, OutputSchema
from models import ReasoningTrace
from embeddings.simple_embedding import SimpleVectorIndex
import uuid

class PipelineController:
    def __init__(self, adapter=None, vector_index=None):
        self.adapter = adapter or MockAdapter()
        self.vector_index = vector_index or SimpleVectorIndex()

    def run(self, user_input: str, request_id: str = None):
        request_id = request_id or str(uuid.uuid4())
        trace = ReasoningTrace(request_id=request_id)

        # Step 1: sanitize input
        s = sanitize_text(user_input)
        trace.add_step("sanitize", {"input": user_input}, {"sanitized": s})

        # Step 2: optionally retrieve context
        ctx = self.vector_index.search(s, top_k=1)
        trace.add_step("retrieve", {"query": s}, {"context": ctx})

        # Step 3: call LLM adapter
        prompt = f"Classify the sentiment of the following text:\n{s}\nContext: {ctx}"
        out = self.adapter.generate(prompt)
        trace.add_step("llm_call", {"prompt": prompt}, {"raw_output": out})

        # Step 4: validate output (pydantic)
        try:
            validated = OutputSchema(
                classification=out.get('classification', 'unknown'),
                confidence=float(out.get('confidence', 0.0)),
                text=out.get('text', '')
            )
            trace.add_step("validate", {}, {"validated": validated.model_dump()})
        except Exception as e:
            trace.add_step("validate_error", {}, {"error": str(e)})
            raise

        # Step 5: return structured result and trace
        return {"request_id": request_id, "result": validated.model_dump(), "trace": trace}
