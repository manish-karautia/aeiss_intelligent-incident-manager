import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# Create Gemini client (NEW SDK)
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL_NAME = "gemini-flash-latest"

class GeminiLLM:
    """
    Minimal LLM wrapper used by all agents.
    Compatible with .invoke() interface.
    """
    def invoke(self, prompt: str):
        response = client.models.generate_content(
            model="gemini-flash-latest",  # FREE + stable
            contents=prompt
        )
        return response.text

llm = GeminiLLM()
