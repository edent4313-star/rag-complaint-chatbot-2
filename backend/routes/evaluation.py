from flask import Blueprint, request, jsonify

from services.evaluation_service import EvaluationService

evaluation_bp = Blueprint("evaluation", __name__, url_prefix="/api")

_service = EvaluationService()


@evaluation_bp.post("/evaluate")
def evaluate():
    """
    POST /api/evaluate

    Body (JSON):
        question      str   required
        answer        str   required
        contexts      list  required  (retrieved document strings)
        ground_truth  str   optional

    Returns JSON with four float scores (0–1):
        faithfulness, answer_relevance, context_precision, context_recall
    """
    body = request.get_json(silent=True) or {}

    question = (body.get("question") or "").strip()
    answer = (body.get("answer") or "").strip()
    contexts = body.get("contexts") or []
    ground_truth = (body.get("ground_truth") or "").strip() or None

    if not question or not answer:
        return jsonify({"error": "Both 'question' and 'answer' are required."}), 400

    if not isinstance(contexts, list):
        contexts = [str(contexts)]

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
