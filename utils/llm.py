import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-flash-latest"

class GeminiLLM:
    def __init__(self):
        self.model = genai.GenerativeModel(MODEL_NAME)

    def invoke(self, prompt: str):
        response = self.model.generate_content(prompt)

        class R:
            content = response.text.strip()

        return R()

llm = GeminiLLM()
