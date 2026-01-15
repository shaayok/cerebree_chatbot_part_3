import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-mpnet-base-v2"
INDEX_PATH = "data/autism.index"
CHUNKS_PATH = "data/autism_tips_chunks.jsonl"
TOP_K = 10

model = SentenceTransformer(MODEL_NAME)
index = faiss.read_index(INDEX_PATH)

with open(CHUNKS_PATH, encoding="utf-8") as f:
    CHUNKS = [json.loads(l) for l in f]

def retrieve_candidates(question: str):
    q_emb = model.encode(question, normalize_embeddings=True)
    D, I = index.search(np.array([q_emb], dtype="float32"), TOP_K)

    return [CHUNKS[i] for i in I[0] if i != -1]
