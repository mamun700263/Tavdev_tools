# ai_service.py
import os
from anthropic import Anthropic
from openai import OpenAI

class AIService:
    def __init__(self):
        self.anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def chat(self, provider: str, message: str) -> str:
        if provider == "claude":
            res = self.anthropic.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1024,
                messages=[{"role": "user", "content": message}]
            )
            return res.content[0].text

        elif provider == "openai":
            res = self.openai.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": message}]
            )
            return res.choices[0].message.content

        else:
            raise ValueError(f"Unknown provider: {provider}")