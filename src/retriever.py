import pandas as pd
import faiss
import numpy as np

from sentence_transformers import (
    SentenceTransformer
)

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "complaint_embeddings.parquet")

df = pd.read_parquet(DATA_PATH)

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(BASE_DIR, "..", "vector_store", "complaints.faiss")

index = faiss.read_index(INDEX_PATH)

'''df = pd.read_parquet(
    "../data/complaint_embeddings.parquet"
)

index = faiss.read_index(
    "../vector_store/complaints.faiss"
)'''

def retrieve(question, top_k=5):

    query_embedding = model.encode(
        [question]
    ).astype("float32")

    faiss.normalize_L2(query_embedding)

    scores, indices = index.search(
        query_embedding,
        top_k
    )

    results = (
        df.iloc[indices[0]]
        .copy()
    )

    results["score"] = scores[0]

    return results