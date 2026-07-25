from src.retriever import retrieve
from src.prompt_template import PromptEngine
from src.generator import generate_answer

def answer_question(question):
    # 1. Retrieve the relevant documents
    retrieved_df = retrieve(question, top_k=5)

    # 2. Extract the text
    context = "\n\n".join(retrieved_df["document"].tolist())

    # 3. Build the prompt
    final_prompt = PromptEngine.format(
        context=context,
        question=question
    )

    # 4. Generate the answer
    answer = generate_answer(final_prompt)

    return answer, retrieved_df