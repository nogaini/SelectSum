import json
import instructor
from openai import OpenAI
from pydantic import BaseModel


class SummaryResponse(BaseModel):
    summary: str
    bullets: list[str]
    title: str


class Summarizer:
    def __init__(self):
        self.client = OpenAI(base_url="http://127.0.0.1:8001/v1", api_key="xxx")
        self.client = instructor.patch(client=self.client)
        self.system_prompt = """You are a helpful assistant that outputs in JSON. You are given transcript text from a video segment. Convert the given text into short bullet points and a title. Don't add escape characters. Directly list the points and the title, don't add additional text before or after it."""

    def summarize(self, prompt: str) -> dict:
        response = self.client.chat.completions.create(
            model="not-using-this",
            response_model=SummaryResponse,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )
        return response
