import os
from dotenv import load_dotenv
from groq import Groq


load_dotenv()


class LLMGenerator:

    def __init__(self):

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY is not set in the .env file."
            )

        self.client = Groq(
            api_key=api_key
        )

        self.model_name = "openai/gpt-oss-120b"

    def generate_answer(
        self,
        question: str,
        context: str
    ) -> str:

        prompt = f"""
You are an AI PDF Research Assistant.

Your task is to answer the user's question using ONLY
the information contained in the provided PDF context.

Follow these rules carefully:

1. Use only the supplied PDF context.
2. Do not use outside knowledge.
3. Do not invent facts.
4. Do not hallucinate information.
5. If the context does not contain enough information,
   say exactly:

I couldn't find enough information in the uploaded document to answer this question.

6. Keep the answer concise but useful.
7. If the context contains relevant page information,
   mention the page number when appropriate.
8. If the question asks for a summary, combine the
   relevant information from the retrieved sections.

PDF CONTEXT:
====================

{context}

====================

USER QUESTION:

{question}

====================

FINAL ANSWER:
"""

        response = self.client.chat.completions.create(
            model=self.model_name,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a grounded PDF question "
                        "answering assistant. You must "
                        "answer only from the supplied "
                        "document context."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.1,

            max_completion_tokens=800
        )

        return (
            response
            .choices[0]
            .message
            .content
            .strip()
        )