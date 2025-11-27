
from typing import List
import hashlib
import math

def embed_text(text: str) -> List[float]:
    # Very small deterministic embedding: use hash bytes to produce a vector of floats
    h = hashlib.md5(text.encode('utf-8')).digest()
    return [b / 255.0 for b in h]

def cosine_sim(a, b):
    dot = sum(x*y for x,y in zip(a,b))
    na = math.sqrt(sum(x*x for x in a))
    nb = math.sqrt(sum(x*x for x in b))
    if na==0 or nb==0:
        return 0.0
    return dot/(na*nb)

class SimpleVectorIndex:
    def __init__(self):
        self.data = []

    def add(self, key: str, text: str):
        self.data.append((key, embed_text(text), text))

    def search(self, query: str, top_k: int = 1):
        qv = embed_text(query)
        scored = [(k, cosine_sim(qv, v), txt) for k,v,txt in self.data]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]
