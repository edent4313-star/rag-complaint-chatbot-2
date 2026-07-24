import os
import pickle
import faiss
import numpy as np


def build_faiss_store(embeddings, chunks_df):

    # Create folder if it doesn't exist
    os.makedirs("../vector_store", exist_ok=True)

    # Convert embeddings to float32
    embeddings = np.array(
        embeddings,
        dtype=np.float32
    )

    # Get embedding dimension
    dimension = embeddings.shape[1]

    # Create FAISS index
    index = faiss.IndexFlatL2(dimension)

    # Add embeddings
    index.add(embeddings)

    # Save index
    faiss.write_index(
        index,
        "../vector_store/faiss_index.bin"
    )

    # Save metadata
    metadata = chunks_df.to_dict(
        orient="records"
    )

    with open(
        "../vector_store/metadata.pkl",
        "wb"
    ) as f:
        pickle.dump(metadata, f)

    print("=" * 50)
    print("FAISS store created successfully")
    print(f"Vectors stored: {len(embeddings)}")
    print(f"Dimension: {dimension}")
    print("=" * 50)

    print(
        os.path.abspath(
            "../vector_store/faiss_index.bin"
        )
    )

    print(
        os.path.abspath(
            "../vector_store/metadata.pkl"
        )
    )