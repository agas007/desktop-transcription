import openai
import os
from core.entities.transcript import Transcript
from core.services.summarization_service import SummarizationService
from app.config import Config

class OpenRouterSummarizer(SummarizationService):
    def __init__(self):
        # OpenRouter uses the OpenAI library format
        api_key = Config.OPENROUTER_API_KEY
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment")
            
        self.client = openai.OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

    def summarize(self, transcript: Transcript) -> str:
        prompt = f"""
Please generate Meeting Minutes from the following transcript.
Follow this format strictly:

[SUMMARY]
...

[KEY POINTS]
...

[ACTION ITEMS]
* [Owner] Task

[DECISIONS]
...

Here is the transcript:
{transcript.text}
"""
        response = self.client.chat.completions.create(
            # Can change to another openrouter model if preferred (e.g. meta-llama/llama-3-8b-instruct)
            model=Config.OPENROUTER_MODEL, 
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes meeting transcripts."},
                {"role": "user", "content": prompt}
            ],
        )
        return response.choices[0].message.content
