from typing import List, Tuple
import os
from openai import OpenAI
import math

def cosine_sim(a: List[float], b: List[float]) -> float:
    dot = sum(x*y for x,y in zip(a,b))
    na = math.sqrt(sum(x*x for x in a))
    nb = math.sqrt(sum(x*x for x in b))
    if na==0 or nb==0:
        return 0.0
    return dot/(na*nb)

class OpenAIIndex:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required.")
        self.client = OpenAI(api_key=self.api_key)
        self.data: List[Tuple[str, List[float], str]] = []

    def _get_embedding(self, text: str) -> List[float]:
        text = text.replace("\n", " ")
        return self.client.embeddings.create(input=[text], model="text-embedding-3-small").data[0].embedding

    def add(self, key: str, text: str):
        vec = self._get_embedding(text)
        self.data.append((key, vec, text))

    def search(self, query: str, top_k: int = 1):
        qv = self._get_embedding(query)
        scored = [(k, cosine_sim(qv, v), txt) for k,v,txt in self.data]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]
