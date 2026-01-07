import json
from utils.llm import llm
from utils.prompts import INCIDENT_PARSE_PROMPT

class NLPAgent:
    def run(self, text):
        response = llm.predict(INCIDENT_PARSE_PROMPT.format(text=text))
        try:
            return json.loads(response)
        except:
            return {"raw_output": response}
