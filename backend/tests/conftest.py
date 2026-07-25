"""
Shared pytest fixtures.

Heavy imports (retriever model, FAISS index, Qwen LLM) are patched out
so tests run fast in CI without requiring GPU/large downloads.
"""
import sys
import types
import pytest

# ── Stub out the heavyweight src modules before any app code imports them ──────

def _make_stub_module(name):
    mod = types.ModuleType(name)
    sys.modules[name] = mod
    return mod


# sentence_transformers stub
st_mod = _make_stub_module("sentence_transformers")


class _FakeST:
    def __init__(self, *a, **kw):
        pass

    def encode(self, texts, convert_to_numpy=False, **kw):
        import numpy as np
        n = len(texts) if isinstance(texts, list) else 1
        arr = np.zeros((n, 384), dtype="float32")
        return arr


st_mod.SentenceTransformer = _FakeST

# faiss stub
faiss_mod = _make_stub_module("faiss")


class _FakeIndex:
    ntotal = 10

    def search(self, vec, k):
        import numpy as np
        return np.ones((1, k), dtype="float32"), np.arange(k, dtype="int64").reshape(1, k)


faiss_mod.read_index = lambda path: _FakeIndex()
faiss_mod.normalize_L2 = lambda x: None

# transformers stub
tr_mod = _make_stub_module("transformers")
tr_mod.AutoTokenizer = type("AutoTokenizer", (), {
    "from_pretrained": classmethod(lambda cls, *a, **kw: _FakeTokenizer())
})
tr_mod.AutoModelForCausalLM = type("AutoModelForCausalLM", (), {
    "from_pretrained": classmethod(lambda cls, *a, **kw: _FakeModel())
})


class _FakeTokenizer:
    eos_token_id = 0

    def __call__(self, *a, **kw):
        import torch
        return {"input_ids": torch.zeros((1, 4), dtype=torch.long)}

    def apply_chat_template(self, *a, **kw):
        return "prompt"

    def decode(self, *a, **kw):
        return "mocked answer"


class _FakeModel:
    device = "cpu"

    def generate(self, **kw):
        import torch
        return torch.zeros((1, 8), dtype=torch.long)


# torch stub (minimal)
try:
    import torch  # use real torch if available
except ImportError:
    torch_mod = _make_stub_module("torch")
    torch_mod.zeros = lambda *a, **kw: [[0] * 8]
    torch_mod.long = int

# pyarrow stub so retriever import doesn't need real parquet file
import unittest.mock as mock
import pandas as pd

_fake_df = pd.DataFrame({
    "document": ["complaint text one", "complaint text two", "complaint text three"],
    "company":  ["Bank A", "Bank B", "Bank C"],
    "product":  ["Mortgage", "Credit card", "Student loan"],
    "issue":    ["Issue A", "Issue B", "Issue C"],
    "state":    ["CA", "TX", "NY"],
    "score":    [0.9, 0.8, 0.7],
})

# Patch pq.read_table to return a fake table
import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd

_fake_df = pd.DataFrame({
    "document": ["complaint text one", "complaint text two", "complaint text three"],
    "company":  ["Bank A", "Bank B", "Bank C"],
    "product":  ["Mortgage", "Credit card", "Student loan"],
    "issue":    ["Issue A", "Issue B", "Issue C"],
    "state":    ["CA", "TX", "NY"],
    "score":    [0.9, 0.8, 0.7],
})

# Build a fake parquet table that includes both 'document' AND 'metadata'
# columns, exactly as the real file does, so retriever.py doesn't KeyError.
# PyArrow needs metadata serialised as strings (JSON), not raw dicts.
import json as _json

_metadata_records = [
    _json.dumps({
        "company": str(_fake_df.at[i, "company"]),
        "product": str(_fake_df.at[i, "product"]),
        "issue":   str(_fake_df.at[i, "issue"]),
        "state":   str(_fake_df.at[i, "state"]),
        "complaint_id": str(i),
        "date_received": "2023-01-01",
        "chunk_index": 0,
        "total_chunks": 1,
        "product_category": str(_fake_df.at[i, "product"]),
        "sub_issue": "",
    })
    for i in range(len(_fake_df))
]
_fake_table_df = pd.DataFrame({
    "document": _fake_df["document"].tolist(),
    "metadata": _metadata_records,          # strings, not dicts
})
_fake_pq_table = pa.Table.from_pandas(_fake_table_df)


@pytest.fixture(autouse=True)
def patch_retriever_io(monkeypatch):
    """Prevent the retriever from reading disk files."""
    monkeypatch.setattr(pq, "read_table", lambda *a, **kw: _fake_pq_table)
    monkeypatch.setattr("faiss.read_index", lambda path: _FakeIndex())


@pytest.fixture
def app():
    """Return a Flask test app with all blueprints registered."""
    # Patch answer_question so chat tests don't run the full RAG pipeline
    import unittest.mock as mock
    with mock.patch("src.rag_pipeline.retrieve", return_value=_fake_df), \
         mock.patch("src.rag_pipeline.generate_answer", return_value="mocked answer"):
        from app import app as flask_app
        flask_app.config["TESTING"] = True
        yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()
