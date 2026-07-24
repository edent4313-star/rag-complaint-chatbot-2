import pandas as pd

from rag_pipeline import answer_question


def evaluate_rag(questions):

    results = []

    for question in questions:

        try:

            answer, retrieved = (
                answer_question(question)
            )

            source = (
                retrieved.iloc[0]
                ["document"]
            )

            results.append(
                {
                    "Question": question,
                    "Generated Answer": answer,
                    "Retrieved Source": source,
                    "Quality Score": "",
                    "Comments": ""
                }
            )

        except Exception as e:

            results.append(
                {
                    "Question": question,
                    "Generated Answer": f"ERROR: {str(e)}",
                    "Retrieved Source": "",
                    "Quality Score": "",
                    "Comments": ""
                }
            )

    return pd.DataFrame(results)