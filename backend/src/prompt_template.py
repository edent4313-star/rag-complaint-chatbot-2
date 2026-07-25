from typing import List


class PromptEngine:
    """Builds prompts for the complaint chatbot."""

    SYSTEM_PROMPT = (
        "You are an AI Financial Complaint Analyst working with real consumer complaint records.\n\n"
        "Your responsibilities:\n"
        "- Answer ONLY using the retrieved complaint documents provided below.\n"
        "- Never invent or hallucinate information not present in the records.\n"
        "- If the answer cannot be found in the retrieved complaints, clearly state:\n"
        '  "The available complaint records do not contain enough information to answer this question."\n'
        "- Identify and summarize common complaint patterns when relevant.\n"
        "- Be concise, professional, and objective.\n"
        "- Cite companies, products, and issues when they are relevant to the answer.\n"
        "- Structure longer answers with bullet points for clarity."
    )

    @classmethod
    def format(cls, context: str, question: str) -> str:
        """Class-method entry point used by rag_pipeline.py."""
        return (
            f"{cls.SYSTEM_PROMPT}\n\n"
            f"---\n"
            f"RETRIEVED COMPLAINT RECORDS:\n{context}\n---\n\n"
            f"USER QUESTION: {question}\n\n"
            f"ANSWER:"
        )

    def build_prompt(self, question: str, contexts: List[str]) -> str:
        """Instance-method: joins context list then delegates to format()."""
        context = "\n\n".join(contexts)
        return self.format(context=context, question=question)
