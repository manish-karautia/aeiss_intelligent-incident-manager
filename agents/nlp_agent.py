import json
import re
from utils.llm import llm
from utils.prompts import INCIDENT_PARSE_PROMPT

class NLPAgent:
    def run(self, text):
        response = llm.invoke(
            INCIDENT_PARSE_PROMPT.format(text=text)
        ).content

        # Remove markdown fences if present
        cleaned = re.sub(r"```json|```", "", response).strip()

        try:
            return json.loads(cleaned)
        except Exception:
            return {
                "raw_text": text,
                "parsed_output": cleaned
            }
