
from pipeline.controller import PipelineController
from adapters.openai_adapter import OpenAIAdapter
from embeddings.simple_embedding import SimpleVectorIndex
import os
from dotenv import load_dotenv

def main():
    load_dotenv()
    idx = SimpleVectorIndex()
    idx.add("doc1", "This product is excellent and works as expected.")
    idx.add("doc2", "The device is not working after a week.")

    # Ensure API key is present
    if not os.environ.get("OPENAI_API_KEY"):
        print("WARNING: OPENAI_API_KEY not found in environment variables.")
        print("Please set it to run with OpenAIAdapter.")
        return

    adapter = OpenAIAdapter()
    controller = PipelineController(adapter=adapter, vector_index=idx)

    user_input = "This is the worst purchase I've ever made!"
    res = controller.run(user_input, request_id='demo-1')
    print('Result:', res['result'])
    print('\nTrace Steps:')
    for s in res['trace'].steps:
        print(f"- {s.step_name}: input={s.input} output={s.output}")

if __name__ == '__main__':
    main()
