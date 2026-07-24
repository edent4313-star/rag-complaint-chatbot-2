from prompt_toolkit import prompt

'''
PROMPT_TEMPLATE = """
You are a financial complaint analyst.

Read the complaint excerpts carefully.

Identify the major issues customers are reporting.

If multiple complaints mention similar issues,
summarize the common themes.

If the context does not contain enough evidence,
respond:

"I do not have enough information."

Context:
{context}

Question:
{question}

Answer:
"""'''
PROMPT_TEMPLATE = """
Answer the question using only the context below.

Context:
{context}

Question:
{question}

Answer:
"""