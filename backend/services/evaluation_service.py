"""
evaluation_service.py
---------------------
Self-contained RAG evaluation using only already-installed libs:
  - sentence-transformers  (semantic similarity)
  - numpy                  (arithmetic)

Metrics computed
────────────────
faithfulness
    Fraction of the answer's sentences grounded in a retrieved context chunk.

answer_relevance
    Cosine similarity between the question embedding and the answer embedding.

context_recall
    How much of the ground-truth answer is covered by the retrieved contexts.
    Falls back to answer-vs-context similarity when no ground truth is given.

context_precision
    Fraction of retrieved chunks relevant to the question (cosine >= threshold).
"""

import numpy as np
from sentence_transformers import SentenceTransformer

_model: SentenceTransformer | None = None
_THRESHOLD = 0.40


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    return _model


def _cosine(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity between two 1-D vectors."""
    a = np.asarray(a, dtype="float32").ravel()
    b = np.asarray(b, dtype="float32").ravel()
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


def _split_sentences(text: str) -> list[str]:
    """Naive sentence splitter — avoids adding nltk as a dependency."""
    import re
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s.strip() for s in sentences if len(s.strip()) > 10]


class EvaluationService:

    def evaluate(
        self,
        question: str,
        answer: str,
        contexts: list[str],
        ground_truth: str | None = None,
    ) -> dict:
        """Return a dict with four float scores, each in [0, 1]."""
        model = _get_model()

        q_emb = np.asarray(
            model.encode(question, convert_to_numpy=True), dtype="float32"
        ).ravel()
        ans_emb = np.asarray(
            model.encode(answer, convert_to_numpy=True), dtype="float32"
        ).ravel()

        if contexts:
            raw = model.encode(contexts, convert_to_numpy=True)
            ctx_embs = np.asarray(raw, dtype="float32")
            if ctx_embs.ndim == 1:
                ctx_embs = ctx_embs.reshape(1, -1)
        else:
            ctx_embs = np.zeros((0, q_emb.shape[0]), dtype="float32")

        answer_relevance = max(0.0, _cosine(q_emb, ans_emb))
        faithfulness = self._faithfulness(model, answer, ctx_embs)
        context_precision = self._context_precision(q_emb, ctx_embs)
        context_recall = self._context_recall(
            model, ground_truth, answer, ctx_embs, ans_emb
        )

        return {
            "faithfulness": round(faithfulness, 3),
            "answer_relevance": round(answer_relevance, 3),
            "context_precision": round(context_precision, 3),
            "context_recall": round(context_recall, 3),
        }

    @staticmethod
    def _faithfulness(
        model: SentenceTransformer,
        answer: str,
        ctx_embs: np.ndarray,
    ) -> float:
        if ctx_embs.shape[0] == 0:
            return 0.0
        sentences = _split_sentences(answer)
        if not sentences:
            return 0.0
        raw = model.encode(sentences, convert_to_numpy=True)
        sent_embs = np.asarray(raw, dtype="float32")
        if sent_embs.ndim == 1:
            sent_embs = sent_embs.reshape(1, -1)
        grounded = sum(
            1 for s_emb in sent_embs
            if max(_cosine(s_emb, c_emb) for c_emb in ctx_embs) >= _THRESHOLD
        )
        return grounded / len(sentences)

    @staticmethod
    def _context_precision(
        q_emb: np.ndarray,
        ctx_embs: np.ndarray,
    ) -> float:
        if ctx_embs.shape[0] == 0:
            return 0.0
        relevant = sum(
            1 for c_emb in ctx_embs
            if _cosine(q_emb, c_emb) >= _THRESHOLD
        )
        return relevant / ctx_embs.shape[0]

    @staticmethod
    def _context_recall(
        model: SentenceTransformer,
        ground_truth: str | None,
        answer: str,
        ctx_embs: np.ndarray,
        ans_emb: np.ndarray,
    ) -> float:
        if ctx_embs.shape[0] == 0:
            return 0.0
        reference = ground_truth if ground_truth and ground_truth.strip() else answer
        sentences = _split_sentences(reference)
        if not sentences:
            return max(_cosine(ans_emb, c_emb) for c_emb in ctx_embs)
        raw = model.encode(sentences, convert_to_numpy=True)
        ref_embs = np.asarray(raw, dtype="float32")
        if ref_embs.ndim == 1:
            ref_embs = ref_embs.reshape(1, -1)
        scores = [
            max(_cosine(r_emb, c_emb) for c_emb in ctx_embs)
            for r_emb in ref_embs
        ]
        return float(np.mean(scores))
