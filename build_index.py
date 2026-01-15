import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

CHUNKS_PATH = "data/autism_tips_chunks.jsonl"
INDEX_PATH = "data/autism.index"
MODEL_NAME = "all-mpnet-base-v2"

def load_chunks():
    with open(CHUNKS_PATH, encoding="utf-8") as f:
        return [json.loads(l) for l in f]

def main():
    model = SentenceTransformer(MODEL_NAME)
    chunks = load_chunks()

    texts = [c["text"] for c in chunks if c.get("text", "").strip()]
    assert texts, "No valid text chunks found"

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(np.array(embeddings, dtype="float32"))

    faiss.write_index(index, INDEX_PATH)
    print(f"Index saved to {INDEX_PATH}")
    print(f"Total chunks indexed: {len(texts)}")

if __name__ == "__main__":
    main()
