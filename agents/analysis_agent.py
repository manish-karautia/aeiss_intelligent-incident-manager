from utils.llm import llm
from utils.prompts import ROOT_CAUSE_PROMPT

class AnalysisAgent:
    def run(self, context):
        response = llm.invoke(
            ROOT_CAUSE_PROMPT.format(context=context)
        )
        return response
