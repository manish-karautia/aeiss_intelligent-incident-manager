from utils.llm import llm
from utils.prompts import ROOT_CAUSE_PROMPT

class AnalysisAgent:
    def run(self, context):
        return llm.predict(
            ROOT_CAUSE_PROMPT.format(context=context)
        )
