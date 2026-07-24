from typing import List


class PromptEngine:
    """
    Builds prompts for the complaint chatbot.
    """

    SYSTEM_PROMPT = """
You are an AI Financial Complaint Analyst.

Your responsibilities are:

- Answer ONLY using the retrieved complaint documents.
- Never invent information.
- If the answer is not found in the retrieved complaints,
  clearly state that the available complaint records do not
  contain enough information.
- Summarize common complaint patterns.
- Be concise and professional.
- Cite the companies and products when relevant.
"""

    def build_prompt(
        self,
        question: str,
        contexts: List[str],
    ) -> str:

        context = "\n\n".join(contexts)

        return f"""
{self.SYSTEM_PROMPT}

Retrieved Complaint Records

{context}

User Question

{question}

Answer:
"""