"""
retriever.py — lazy-loaded FAISS retriever.

All I/O (parquet read, FAISS index load, model load) is deferred until
the first call to retrieve(). This allows pytest to patch pq.read_table
and faiss.read_index before any real disk access happens.
"""
import json as _json
import os

import faiss
import pandas as pd
import pyarrow.parquet as pq
from sentence_transformers import SentenceTransformer

# ── Paths ──────────────────────────────────────────────────────────────────────
_SRC_DIR = os.path.dirname(os.path.abspath(__file__))
_BASE_DIR = os.path.dirname(_SRC_DIR)

DATA_PATH = os.path.join(_BASE_DIR, "data", "complaint_embeddings.parquet")
INDEX_PATH = os.path.join(_BASE_DIR, "vector_store", "complaints.faiss")

# ── Lazy singletons ────────────────────────────────────────────────────────────
_model = None
_df = None
_index = None


def _load():
    """Load model, parquet, and FAISS index on first use."""
    global _model, _df, _index

    if _model is None:
        print("[retriever] Loading sentence-transformer model…")
        _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    if _df is None:
        print("[retriever] Loading parquet (document + metadata columns only)…")
        table = pq.read_table(DATA_PATH, columns=["document", "metadata"])
        df = table.to_pandas()

        raw_metadata = df["metadata"].tolist()
        if raw_metadata and isinstance(raw_metadata[0], str):
            raw_metadata = [_json.loads(m) for m in raw_metadata]
        metadata_df = pd.json_normalize(raw_metadata)
        _df = pd.concat(
            [df[["document"]].reset_index(drop=True),
             metadata_df.reset_index(drop=True)],
            axis=1,
        )
        print(f"[retriever] Loaded {len(_df):,} complaint records.")

    if _index is None:
        print("[retriever] Loading FAISS index…")
        _index = faiss.read_index(INDEX_PATH)
        print(f"[retriever] FAISS index ready — {_index.ntotal:,} vectors.")


def retrieve(question: str, top_k: int = 5) -> pd.DataFrame:
    """Encode *question*, search FAISS, return top_k records with a score column."""
    _load()

    query_vec = _model.encode([question]).astype("float32")
    faiss.normalize_L2(query_vec)

    scores, indices = _index.search(query_vec, top_k)

    results = _df.iloc[indices[0]].copy()
    results["score"] = scores[0]
    results = results.reset_index(drop=True)
    return results
