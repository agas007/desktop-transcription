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
            default_headers={
                "HTTP-Referer": "https://github.com/agas/desktop-transcription",
                "X-Title": "Desktop Transcription MVP",
            }
        )

    def summarize(self, transcript: Transcript) -> str:
        prompt = f"""
Tolong buatkan Notulensi Rapat (Meeting Minutes) dalam Bahasa Indonesia dari transkrip berikut ini.
Gunakan format yang terstruktur dengan ketat seperti di bawah ini:

[RINGKASAN]
...

[POIN PENTING]
...

[TINDAKAN / ACTION ITEMS]
* [Pihak Terkait] Tugas / Action Item

[KEPUTUSAN]
...

Berikut adalah transkripnya:
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
