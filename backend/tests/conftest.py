"""
Shared pytest fixtures.

Heavy imports (retriever model, FAISS index, Qwen LLM) are patched out
so tests run fast in CI without requiring GPU/large downloads.
"""
import json as _json
import sys
import types
import unittest.mock as mock

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import pytest


# ── Stub heavyweight src modules before any app code imports them ──────────────

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
        n = len(texts) if isinstance(texts, list) else 1
        return np.zeros((n, 384), dtype="float32")


st_mod.SentenceTransformer = _FakeST


# faiss stub
faiss_mod = _make_stub_module("faiss")


class _FakeIndex:
    ntotal = 10

    def search(self, vec, k):
        scores = np.ones((1, k), dtype="float32")
        indices = np.arange(k, dtype="int64").reshape(1, k)
        return scores, indices


faiss_mod.read_index = lambda path: _FakeIndex()
faiss_mod.normalize_L2 = lambda x: None


# transformers stub
tr_mod = _make_stub_module("transformers")


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


tr_mod.AutoTokenizer = type("AutoTokenizer", (), {
    "from_pretrained": classmethod(lambda cls, *a, **kw: _FakeTokenizer()),
})
tr_mod.AutoModelForCausalLM = type("AutoModelForCausalLM", (), {
    "from_pretrained": classmethod(lambda cls, *a, **kw: _FakeModel()),
})


# torch — use real if available, else stub
try:
    import torch  # noqa: F401 (used by _FakeTokenizer/_FakeModel above)
except ImportError:
    torch_mod = _make_stub_module("torch")
    torch_mod.zeros = lambda *a, **kw: [[0] * 8]
    torch_mod.long = int


# ── Fake parquet table ─────────────────────────────────────────────────────────

_fake_df = pd.DataFrame({
    "document": ["complaint text one", "complaint text two", "complaint text three"],
    "company": ["Bank A", "Bank B", "Bank C"],
    "product": ["Mortgage", "Credit card", "Student loan"],
    "issue": ["Issue A", "Issue B", "Issue C"],
    "state": ["CA", "TX", "NY"],
    "score": [0.9, 0.8, 0.7],
})

_metadata_records = [
    _json.dumps({
        "company": str(_fake_df.at[i, "company"]),
        "product": str(_fake_df.at[i, "product"]),
        "issue": str(_fake_df.at[i, "issue"]),
        "state": str(_fake_df.at[i, "state"]),
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
    "metadata": _metadata_records,
})
_fake_pq_table = pa.Table.from_pandas(_fake_table_df)


# ── Fixtures ───────────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def patch_retriever_io(monkeypatch):
    """Patch parquet and FAISS reads so no files are needed."""
    monkeypatch.setattr(pq, "read_table", lambda *a, **kw: _fake_pq_table)
    monkeypatch.setattr("faiss.read_index", lambda path: _FakeIndex())


@pytest.fixture
def app():
    """Flask test app with all blueprints; RAG pipeline mocked."""
    with mock.patch("src.rag_pipeline.retrieve", return_value=_fake_df), \
         mock.patch("src.rag_pipeline.generate_answer", return_value="mocked answer"):
        from app import app as flask_app
        flask_app.config["TESTING"] = True
        yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()
