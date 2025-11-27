12IQ Practice Project - Deterministic Reasoning Pipeline
=======================================================

This practice project demonstrates a minimal, well-structured reasoning pipeline
with adapters, helpers, deterministic behavior, tracing, and tests — matching the
expectations for an infrastructure-level AI internship.

Project structure:
- adapters/         : Adapter classes (Mock + example OpenAI-style stub)
- helpers/          : Utility functions (sanitize, validators, logging)
- pipeline/         : Controller orchestrating the reasoning steps
- embeddings/       : Simple mock embedding interface + vector search stub
- models.py         : Dataclasses for typed messages and traces
- tests/            : pytest tests that mock adapters for deterministic testing
- run_demo.py       : Small demo runner showing a pipeline execution
- requirements.txt  : Minimal dependencies

Reference: Your CV uploaded at /mnt/data/Selva_Ganapathy_Elangovan.pdf
(kept outside the project folder; path included here for traceability).

How to run:
1. (Optional) Create a virtualenv and install dependencies:
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

2. Run the demo:
   python run_demo.py

3. Run tests:
   pip install pytest
   pytest -q

Notes:
- The OpenAI adapter is a stub showing how to adapt vendor SDKs; it is not functional.
- The MockAdapter provides deterministic responses and is used in tests.