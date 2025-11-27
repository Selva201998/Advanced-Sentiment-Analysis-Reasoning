
from pipeline.controller import PipelineController
from adapters.mock_adapter import MockAdapter
from embeddings.simple_embedding import SimpleVectorIndex

def test_pipeline_deterministic():
    idx = SimpleVectorIndex()
    idx.add("a", "Good product")
    adapter = MockAdapter()
    controller = PipelineController(adapter=adapter, vector_index=idx)

    in_text = "This is a good product."
    res1 = controller.run(in_text, request_id='t1')
    res2 = controller.run(in_text, request_id='t1')

    assert res1['result'] == res2['result']
    assert res1['request_id'] == res2['request_id']
    assert len(res1['trace'].steps) >= 3
