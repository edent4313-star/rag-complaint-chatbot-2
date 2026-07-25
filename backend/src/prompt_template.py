from typing import List


class PromptEngine:
    """
    Builds prompts for the complaint chatbot using a structured,
    prompt-engineered template.
    """

    SYSTEM_PROMPT = """You are an AI Financial Complaint Analyst working with real consumer complaint records.

Your responsibilities:
- Answer ONLY using the retrieved complaint documents provided below.
- Never invent or hallucinate information not present in the records.
- If the answer cannot be found in the retrieved complaints, clearly state:
  "The available complaint records do not contain enough information to answer this question."
- Identify and summarize common complaint patterns when relevant.
- Be concise, professional, and objective.
- Cite companies, products, and issues when they are relevant to the answer.
- Structure longer answers with bullet points for clarity."""

    @classmethod
    def format(
        cls,
        context: str,
        question: str,
    ) -> str:
        """
        Class-method entry point used by rag_pipeline.py.
        Accepts a pre-joined context string and a question.
        """
        return f"""{cls.SYSTEM_PROMPT}

---
RETRIEVED COMPLAINT RECORDS:
{context}
---

USER QUESTION: {question}

ANSWER:"""

    def build_prompt(
        self,
        question: str,
        contexts: List[str],
    ) -> str:
        """
        Instance-method entry point — joins a list of context strings
        then delegates to the class-method formatter.
        """
        context = "\n\n".join(contexts)
        return self.format(context=context, question=question)