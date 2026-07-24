from flask import Blueprint
from flask import request

from services.chat_service import chat_service

chat_bp = Blueprint(
    "chat",
    __name__,
    url_prefix="/api"
)


@chat_bp.post("/chat")
def chat():

    body = request.get_json()

    question = body["question"]

    return chat_service.ask(question)