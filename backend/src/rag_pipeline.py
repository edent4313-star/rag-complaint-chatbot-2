from src.retriever import retrieve
from src.prompt_template import PromptEngine
from src.generator import generate_answer


def answer_question(question):
    retrieved_df = retrieve(question, top_k=5)
    context = "\n\n".join(retrieved_df["document"].tolist())
    final_prompt = PromptEngine.format(context=context, question=question)
    answer = generate_answer(final_prompt)
    return answer, retrieved_df
