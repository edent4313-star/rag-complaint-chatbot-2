'''from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

VECTOR_STORE = BASE_DIR / "vector_store"

TOP_K = 5

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2" '''

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = BASE_DIR / "data" / "complaints.csv"

VECTOR_STORE = BASE_DIR / "vector_store"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

TOP_K = 5