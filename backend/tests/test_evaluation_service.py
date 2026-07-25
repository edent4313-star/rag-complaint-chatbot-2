"""
Unit tests for EvaluationService.
Heavy ML deps are stubbed in conftest.py — no network or GPU required.
"""
import numpy as np
import pytest
from unittest.mock import MagicMock, patch

from services.evaluation_service import EvaluationService, _cosine, _split_sentences


# ── Helper function tests ──────────────────────────────────────────────────────

class TestCosine:

    def test_identical_vectors_return_one(self):
        v = np.array([1.0, 0.0, 0.0])
        assert abs(_cosine(v, v) - 1.0) < 1e-6

    def test_orthogonal_vectors_return_zero(self):
        a = np.array([1.0, 0.0])
        b = np.array([0.0, 1.0])
        assert abs(_cosine(a, b)) < 1e-6

    def test_zero_vector_returns_zero(self):
        z = np.array([0.0, 0.0])
        v = np.array([1.0, 0.0])
        assert _cosine(z, v) == 0.0

    def test_opposite_vectors_return_minus_one(self):
        a = np.array([1.0, 0.0])
        b = np.array([-1.0, 0.0])
        assert abs(_cosine(a, b) - (-1.0)) < 1e-6


class TestSplitSentences:

    def test_splits_on_period(self):
        text = "First sentence. Second sentence. Third sentence."
        parts = _split_sentences(text)
        assert len(parts) >= 2

    def test_splits_on_question_mark(self):
        text = "Is this right? Yes it is. Definitely."
        parts = _split_sentences(text)
        assert len(parts) >= 2

    def test_short_fragments_filtered(self):
        parts = _split_sentences("Hi. Ok. This is a proper sentence.")
        for p in parts:
            assert len(p) >= 10

    def test_empty_string_returns_empty(self):
        assert _split_sentences("") == []


# ── EvaluationService fixtures ─────────────────────────────────────────────────

@pytest.fixture
def svc():
    return EvaluationService()


@pytest.fixture
def mock_model():
    """Fake SentenceTransformer with consistent 4-D unit vectors."""
    m = MagicMock()

    def _encode(texts, convert_to_numpy=False, **kw):
        if isinstance(texts, str):
            texts = [texts]
        n = len(texts)
        dim = 4
        arr = np.zeros((n, dim), dtype="float32")
        for i in range(n):
            arr[i, 0] = 1.0
        return arr[0] if n == 1 else arr

    m.encode.side_effect = _encode
    return m


# ── Output shape tests ─────────────────────────────────────────────────────────

class TestEvaluationServiceOutputShape:

    def test_returns_four_metrics(self, svc, mock_model):
        with patch("services.evaluation_service._get_model", return_value=mock_model), \
             patch("services.evaluation_service._split_sentences",
                   return_value=["sentence one about complaints."]):
            scores = svc.evaluate(
                question="What are common complaints?",
                answer="Customers complain about fees.",
                contexts=["Many customers report hidden fees on accounts."],
            )
        assert set(scores.keys()) == {
            "faithfulness", "answer_relevance",
            "context_precision", "context_recall",
        }

    def test_all_scores_between_zero_and_one(self, svc, mock_model):
        with patch("services.evaluation_service._get_model", return_value=mock_model), \
             patch("services.evaluation_service._split_sentences",
                   return_value=["mortgage customers face loan modification denials."]):
            scores = svc.evaluate(
                question="What are mortgage issues?",
                answer="Mortgage customers face loan modification denials.",
                contexts=[
                    "Borrowers report loan modification denials.",
                    "Foreclosure proceedings despite timely payments.",
                ],
            )
        for key, val in scores.items():
            assert 0.0 <= val <= 1.0, f"{key} = {val} out of [0, 1]"

    def test_scores_are_rounded_to_three_decimals(self, svc, mock_model):
        with patch("services.evaluation_service._get_model", return_value=mock_model), \
             patch("services.evaluation_service._split_sentences",
                   return_value=["a sentence."]):
            scores = svc.evaluate(question="q", answer="a", contexts=["ctx"])
        for key, val in scores.items():
            assert val == round(val, 3), f"{key} not rounded: {val}"


# ── Edge case tests ────────────────────────────────────────────────────────────

class TestEvaluationServiceEdgeCases:

    def test_empty_contexts_returns_zeros_for_context_metrics(self, svc, mock_model):
        with patch("services.evaluation_service._get_model", return_value=mock_model):
            scores = svc.evaluate(question="q", answer="a", contexts=[])
        assert scores["faithfulness"] == 0.0
        assert scores["context_precision"] == 0.0
        assert scores["context_recall"] == 0.0

    def test_with_ground_truth(self, svc, mock_model):
        with patch("services.evaluation_service._get_model", return_value=mock_model), \
             patch("services.evaluation_service._split_sentences",
                   return_value=["customers report unauthorized charges."]):
            scores = svc.evaluate(
                question="What are credit card complaints?",
                answer="Customers dispute unauthorized charges.",
                contexts=["Unauthorized charges are reported frequently."],
                ground_truth="Customers report unauthorized charges on credit cards.",
            )
        assert isinstance(scores["context_recall"], float)

    def test_identical_answer_and_question_high_relevance(self, svc, mock_model):
        """Identical question and answer → cosine similarity = 1.0."""
        with patch("services.evaluation_service._get_model", return_value=mock_model), \
             patch("services.evaluation_service._split_sentences",
                   return_value=["what are credit card complaints?"]):
            scores = svc.evaluate(
                question="What are credit card complaints?",
                answer="What are credit card complaints?",
                contexts=["Credit card issues are frequently reported."],
            )
        assert scores["answer_relevance"] == 1.0
