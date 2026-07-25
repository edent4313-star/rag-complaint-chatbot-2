"""
Integration tests for the chat and evaluate routes.
The RAG pipeline (retriever + LLM) is mocked so no models are loaded.
conftest.py's autouse fixture patches the parquet/faiss reads.
"""
import json

import pandas as pd
import pytest
from unittest.mock import patch

FAKE_SOURCES = pd.DataFrame({
    "document": ["complaint about fees", "another complaint"],
    "company": ["Bank A", "Bank B"],
    "product": ["Mortgage", "Credit card"],
    "issue": ["Billing", "Fraud"],
    "state": ["CA", "TX"],
    "score": [0.9, 0.8],
})


@pytest.fixture
def client():
    """Flask test client with the RAG pipeline fully mocked."""
    with patch("src.rag_pipeline.retrieve", return_value=FAKE_SOURCES), \
         patch("src.rag_pipeline.generate_answer", return_value="mocked answer"):
        from app import app
        app.config["TESTING"] = True
        yield app.test_client()


class TestChatEndpoint:

    def _post(self, client, body):
        return client.post(
            "/api/chat",
            data=json.dumps(body),
            content_type="application/json",
        )

    def test_valid_question_returns_200(self, client):
        res = self._post(client, {"question": "What are mortgage complaints?"})
        assert res.status_code == 200

    def test_response_has_answer_key(self, client):
        data = self._post(client, {"question": "test"}).get_json()
        assert "answer" in data

    def test_response_has_sources_key(self, client):
        data = self._post(client, {"question": "test"}).get_json()
        assert "sources" in data

    def test_sources_is_a_list(self, client):
        data = self._post(client, {"question": "test"}).get_json()
        assert isinstance(data["sources"], list)

    def test_answer_is_mocked_string(self, client):
        data = self._post(client, {"question": "test"}).get_json()
        assert data["answer"] == "mocked answer"

    def test_empty_question_returns_fallback(self, client):
        res = self._post(client, {"question": ""})
        assert res.status_code == 200
        assert len(res.get_json()["answer"]) > 0

    def test_missing_question_key_returns_fallback(self, client):
        res = self._post(client, {})
        assert res.status_code == 200
        assert "answer" in res.get_json()

    def test_non_json_body_handled_gracefully(self, client):
        res = client.post("/api/chat", data="not json", content_type="text/plain")
        assert res.status_code == 200


class TestEvaluateEndpoint:

    def _post(self, client, body):
        return client.post(
            "/api/evaluate",
            data=json.dumps(body),
            content_type="application/json",
        )

    def test_valid_payload_returns_200(self, client):
        res = self._post(client, {
            "question": "What are mortgage complaints?",
            "answer": "Customers complain about loan modifications.",
            "contexts": ["Loan modification denials are common."],
        })
        assert res.status_code == 200

    def test_response_has_all_four_metrics(self, client):
        data = self._post(client, {
            "question": "q",
            "answer": "a",
            "contexts": ["ctx"],
        }).get_json()
        for key in ("faithfulness", "answer_relevance", "context_precision", "context_recall"):
            assert key in data, f"Missing metric: {key}"

    def test_missing_question_returns_400(self, client):
        res = self._post(client, {"answer": "a", "contexts": ["ctx"]})
        assert res.status_code == 400

    def test_missing_answer_returns_400(self, client):
        res = self._post(client, {"question": "q", "contexts": ["ctx"]})
        assert res.status_code == 400

    def test_empty_contexts_returns_200(self, client):
        res = self._post(client, {"question": "q", "answer": "a", "contexts": []})
        assert res.status_code == 200

    def test_with_ground_truth(self, client):
        res = self._post(client, {
            "question": "q",
            "answer": "a",
            "contexts": ["ctx"],
            "ground_truth": "ideal answer",
        })
        assert res.status_code == 200
        assert "context_recall" in res.get_json()
