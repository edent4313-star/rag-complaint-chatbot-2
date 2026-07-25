"""
evaluation_service.py
---------------------
Self-contained RAG evaluation using only already-installed libs:
  - sentence-transformers  (semantic similarity)
  - numpy                  (arithmetic)

Metrics computed
────────────────
faithfulness
    What fraction of the answer's sentences can be semantically
    grounded in at least one retrieved context chunk.
    Score = (sentences with a context match ≥ threshold) / total sentences

answer_relevance
    Cosine similarity between the question embedding and the
    answer embedding.  High score ⟹ the answer is on-topic.

context_recall   (requires ground_truth; falls back to answer similarity)
    How much of the ground-truth answer is covered by the retrieved
    contexts.  Score = avg max-similarity of each ground-truth sentence
    against the context pool.

context_precision
    Signal-to-noise of the retrieved set: what fraction of the
    retrieved chunks are actually relevant to the question.
    Score = fraction of chunks whose similarity to the question ≥ threshold.
"""

import numpy as np
from sentence_transformers import SentenceTransformer

# Reuse the same model already loaded by the retriever where possible.
# We load lazily so the service module itself is cheap to import.
_model: SentenceTransformer | None = None
_THRESHOLD = 0.40          # cosine similarity threshold for "relevant"


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    return _model


def _cosine(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity between two 1-D vectors."""
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


def _split_sentences(text: str) -> list[str]:
    """Naive sentence splitter — avoids adding nltk as a dependency."""
    import re
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s.strip() for s in sentences if len(s.strip()) > 10]


# ─── public API ───────────────────────────────────────────────────────────────

class EvaluationService:

    def evaluate(
        self,
        question: str,
        answer: str,
        contexts: list[str],
        ground_truth: str | None = None,
    ) -> dict:
        """
        Returns a dict with four float scores, each in [0, 1].
        """
        model = _get_model()

        # ── encode everything ────────────────────────────────────────────────
        q_emb   = model.encode(question,   convert_to_numpy=True)
        ans_emb = model.encode(answer,     convert_to_numpy=True)
        ctx_embs = model.encode(contexts,  convert_to_numpy=True) \
                   if contexts else np.zeros((0, q_emb.shape[0]))

        # ── 1. answer_relevance ──────────────────────────────────────────────
        answer_relevance = max(0.0, _cosine(q_emb, ans_emb))

        # ── 2. faithfulness ──────────────────────────────────────────────────
        faithfulness = self._faithfulness(model, answer, ctx_embs)

        # ── 3. context_precision ─────────────────────────────────────────────
        context_precision = self._context_precision(q_emb, ctx_embs)

        # ── 4. context_recall ────────────────────────────────────────────────
        context_recall = self._context_recall(
            model, ground_truth, answer, ctx_embs, ans_emb
        )

        return {
            "faithfulness":       round(faithfulness,       3),
            "answer_relevance":   round(answer_relevance,   3),
            "context_precision":  round(context_precision,  3),
            "context_recall":     round(context_recall,     3),
        }

    # ── private helpers ───────────────────────────────────────────────────────

    @staticmethod
    def _faithfulness(
        model: SentenceTransformer,
        answer: str,
        ctx_embs: np.ndarray,
    ) -> float:
        """Fraction of answer sentences grounded in a context chunk."""
        if ctx_embs.shape[0] == 0:
            return 0.0
        sentences = _split_sentences(answer)
        if not sentences:
            return 0.0
        sent_embs = model.encode(sentences, convert_to_numpy=True)
        grounded = 0
        for s_emb in sent_embs:
            sims = [_cosine(s_emb, c_emb) for c_emb in ctx_embs]
            if max(sims) >= _THRESHOLD:
                grounded += 1
        return grounded / len(sentences)

    @staticmethod
    def _context_precision(
        q_emb: np.ndarray,
        ctx_embs: np.ndarray,
    ) -> float:
        """Fraction of retrieved chunks that are relevant to the question."""
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
        """
        If ground_truth provided: avg max-similarity of each GT sentence
        against the context pool.
        Otherwise: cosine similarity of the answer against the context pool
        (proxy for 'did the context support the answer').
        """
        if ctx_embs.shape[0] == 0:
            return 0.0

        reference = ground_truth if ground_truth and ground_truth.strip() else answer
        sentences = _split_sentences(reference)

        if not sentences:
            # fall back to answer-vs-context similarity
            sims = [_cosine(ans_emb, c_emb) for c_emb in ctx_embs]
            return max(sims)

        ref_embs = model.encode(sentences, convert_to_numpy=True)
        scores = []
        for r_emb in ref_embs:
            sims = [_cosine(r_emb, c_emb) for c_emb in ctx_embs]
            scores.append(max(sims))
        return float(np.mean(scores))
