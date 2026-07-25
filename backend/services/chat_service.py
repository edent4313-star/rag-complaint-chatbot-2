from src.rag_pipeline import answer_question


class ChatService:

    def __init__(self):
        pass

    def get_chat_response(self, question):
        question = (question or "").strip()

        if not question:
            return {
                "answer": "Please ask a question about the complaints data.",
                "sources": [],
            }

        try:
            answer, retrieved_df = answer_question(question)
            sources = (
                retrieved_df.to_dict(orient="records")
                if retrieved_df is not None
                else []
            )
            return {"answer": answer, "sources": sources}
        except Exception as exc:
            return {
                "answer": f"Sorry, I could not generate a response right now. {exc}",
                "sources": [],
            }
