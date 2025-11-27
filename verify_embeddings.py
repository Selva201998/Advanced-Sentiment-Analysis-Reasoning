import os
from dotenv import load_dotenv
from embeddings.openai_embedding import OpenAIIndex

load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    print("Skipping test: No OPENAI_API_KEY found.")
    exit(0)

print("Initializing OpenAIIndex...")
idx = OpenAIIndex()
idx.add("apple", "Apples are red and delicious fruits.")
idx.add("banana", "Bananas are yellow and long.")
idx.add("car", "Cars are vehicles with four wheels.")

print("Searching for 'fruit'...")
results = idx.search("fruit", top_k=2)
for k, score, txt in results:
    print(f"Match: {k} (score: {score:.4f})")

assert "apple" in [r[0] for r in results] or "banana" in [r[0] for r in results]
print("Verification passed!")
