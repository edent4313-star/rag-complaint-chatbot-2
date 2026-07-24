from src.rag_pipeline import RAGPipeline


class ChatService:

    def __init__(self):

        self.pipeline = RAGPipeline()

    def ask(self, question):

        answer, sources = self.pipeline.query(question)

        return {

            "question": question,

            "answer": answer,

            "sources": sources

        }


chat_service = ChatService()