from openai import OpenAI
from django.conf import settings


class OpenAILLM:
    def __init__(self, model="gpt-4o-mini"):
        api_key = getattr(settings, "OPENAI_API_KEY", None)

        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY is not set. Check your .env and settings.py"
            )

        self.client = OpenAI(api_key=api_key)
        self.model = model

    def __call__(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert CAD/CAE research assistant.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content
