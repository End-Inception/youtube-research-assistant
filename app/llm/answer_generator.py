from google import genai
from google.genai import types

from app.config import GEMINI_API_KEY, LLM_MODEL


class AnswerGenerator:

    def __init__(self):

        if not GEMINI_API_KEY:
            raise ValueError("Missing GEMINI_API_KEY")

        # Initialize Gemini client once
        self.client = genai.Client(
            api_key=GEMINI_API_KEY,
            http_options=types.HttpOptions(
                retry_options=types.HttpRetryOptions(
                    attempts=5,
                    initial_delay=2.0,
                    max_delay=30.0,
                    exp_base=2.0,
                    jitter=1.0
                )
            )
        )

        self.model = LLM_MODEL

    def generate_answer(self, question: str, retrieved_results: list):

        """
        Generate an answer using retrieved YouTube transcript chunks.
        """

        if not question.strip():
            raise ValueError("Question cannot be empty.")

        if not retrieved_results:
            return {
                "answer": "I could not find relevant information in the available transcripts.",
                "sources": []
            }

        # Prepare context from retrieved transcript chunks
        context_parts = []

        for i, result in enumerate(retrieved_results, start=1):

            chunk = result["chunk"]

            source_text = f"""
Source {i}
Video ID: {chunk['video_id']}
Start time: {chunk['start_time']}
End time: {chunk['end_time']}
Transcript: {chunk['text']}
"""

            context_parts.append(source_text)

        context = "\n".join(context_parts)

        prompt = f"""
You are a YouTube research assistant.

Answer the user's question using ONLY the transcript context provided below.

Instructions:
1. Give a clear and useful answer.
2. Do not invent facts that are not present in the context.
3. If the context does not contain enough information, clearly say so.
4. Cite supporting information using [Source 1], [Source 2], etc.
5. Only cite sources that actually support the statement.
6. Explain the answer in simple language.
7. Do not invent video IDs or timestamps.

USER QUESTION:
{question}

RETRIEVED TRANSCRIPT CONTEXT:
{context}

Write the answer:
"""

        response = self.client.interactions.create(
            model=self.model,
            input=prompt
        )

        if not response.output_text:
            raise RuntimeError("Gemini returned an empty response.")

        return {
            "answer": response.output_text,
            "sources": retrieved_results
        }