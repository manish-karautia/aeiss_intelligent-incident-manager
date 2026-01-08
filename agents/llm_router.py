# agents/llm_router.py
from utils.llm import llm  # Gemini LLM

class LLMRouter:
    def get_llm(self, task: str):
        """
        Routes tasks to an appropriate LLM.
        Currently uses Gemini for all tasks.
        Can be extended later to support Ollama.
        """
        return llm
