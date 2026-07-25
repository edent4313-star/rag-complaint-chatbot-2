from flask import Blueprint, request, jsonify

from services.evaluation_service import EvaluationService

evaluation_bp = Blueprint(
    "evaluation",
    __name__,
    url_prefix="/api"
)

_service = EvaluationService()


@evaluation_bp.post("/evaluate")
def evaluate():
    """
    POST /api/evaluate
    Body (JSON):
      {
        "question":     "...",          required
        "answer":       "...",          required
        "contexts":     ["...", ...],   required  (list of retrieved doc strings)
        "ground_truth": "..."           optional
      }
    Returns:
      {
        "faithfulness":      0.0–1.0,
        "answer_relevance":  0.0–1.0,
        "context_precision": 0.0–1.0,
        "context_recall":    0.0–1.0
      }
    """
    body = request.get_json(silent=True) or {}

    question     = (body.get("question")     or "").strip()
    answer       = (body.get("answer")       or "").strip()
    contexts     = body.get("contexts")      or []
    ground_truth = (body.get("ground_truth") or "").strip() or None

    if not question or not answer:
        return jsonify({"error": "Both 'question' and 'answer' are required."}), 400

    if not isinstance(contexts, list):
        contexts = [str(contexts)]

    # Filter out blank/None context strings
    contexts = [str(c) for c in contexts if c and str(c).strip()]

    try:
        scores = _service.evaluate(
            question=question,
            answer=answer,
            contexts=contexts,
            ground_truth=ground_truth,
        )
        return jsonify(scores)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500
