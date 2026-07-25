import os

import faiss
import numpy as np
import pandas as pd
import pyarrow.parquet as pq
from sentence_transformers import SentenceTransformer

# ── Paths ──────────────────────────────────────────────────────────────────────
_SRC_DIR  = os.path.dirname(os.path.abspath(__file__))
_BASE_DIR = os.path.dirname(_SRC_DIR)

DATA_PATH  = os.path.join(_BASE_DIR, "data", "complaint_embeddings.parquet")
INDEX_PATH = os.path.join(_BASE_DIR, "vector_store", "complaints.faiss")

# ── Load embedding model ───────────────────────────────────────────────────────
print("[retriever] Loading sentence-transformer model…")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# ── Load parquet WITHOUT the embedding column (saves ~7 GB RAM) ───────────────
print("[retriever] Loading parquet (document + metadata columns only)…")
table = pq.read_table(DATA_PATH, columns=["document", "metadata"])
df = table.to_pandas()

# Flatten the metadata dict column into separate DataFrame columns
metadata_df = pd.json_normalize(df["metadata"].tolist())
df = pd.concat([df[["document"]].reset_index(drop=True),
                metadata_df.reset_index(drop=True)], axis=1)

print(f"[retriever] Loaded {len(df):,} complaint records.")

# ── Load FAISS index ───────────────────────────────────────────────────────────
print("[retriever] Loading FAISS index…")
index = faiss.read_index(INDEX_PATH)
print(f"[retriever] FAISS index ready — {index.ntotal:,} vectors.")


def retrieve(question: str, top_k: int = 5) -> pd.DataFrame:
    """
    Encode *question*, search the FAISS index, and return a DataFrame of
    the top_k matching complaint records with an added 'score' column.
    """
    query_vec = model.encode([question]).astype("float32")
    faiss.normalize_L2(query_vec)

    scores, indices = index.search(query_vec, top_k)

    results = df.iloc[indices[0]].copy()
    results["score"] = scores[0]
    results = results.reset_index(drop=True)

    return results
