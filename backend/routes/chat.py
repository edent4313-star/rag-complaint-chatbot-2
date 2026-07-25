from flask import Blueprint, request

from services.chat_service import ChatService

chat_bp = Blueprint(
    "chat",
    __name__,
    url_prefix="/api"
)

service = ChatService()


@chat_bp.post("/chat")
def chat():
    body = request.get_json(silent=True) or {}
    question = body.get("question", "")
    return service.get_chat_response(question)