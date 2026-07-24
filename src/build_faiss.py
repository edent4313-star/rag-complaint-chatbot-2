import pandas as pd
import numpy as np
import faiss

print("Loading parquet...")
df = pd.read_parquet(
    "data/complaint_embeddings.parquet"
)

print("Preparing embeddings...")
embeddings = np.vstack(
    df["embedding"].values
).astype("float32")

# Normalize for cosine similarity
faiss.normalize_L2(embeddings)

dimension = embeddings.shape[1]

print("Building FAISS index...")
index = faiss.IndexFlatIP(dimension)

index.add(embeddings)

print("Saving index...")
faiss.write_index(
    index,
    "vector_store/complaints.faiss"
)

print("Done!")
print("Vectors:", index.ntotal)