from src.retriever import retrieve
from src.prompt_template import PROMPT_TEMPLATE
from src.generator import generate_answer

from src.retriever import retrieve
from src.generator import generate_answer



def answer_question(question):

    retrieved_df = retrieve(question, top_k=5)

    context = "\n\n".join(
        retrieved_df["document"].tolist()
    )

    final_prompt = PROMPT_TEMPLATE.format(
        context=context,
        question=question
    )

    answer = generate_answer(final_prompt)

    return answer, retrieved_df


def run_rag(question):

    retrieved_chunks = retrieve(question)

    context = "\n\n".join(
        retrieved_chunks["document"].tolist()
    )

    final_prompt = PROMPT_TEMPLATE.format(
        context=context,
        question=question
    )

    answer = generate_answer(final_prompt)

    return answer, retrieved_chunks