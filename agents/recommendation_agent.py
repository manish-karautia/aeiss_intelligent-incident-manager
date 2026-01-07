from utils.llm import llm
from utils.prompts import RECOMMENDATION_PROMPT

class RecommendationAgent:
    def run(self, context, root_cause):
        return llm.predict(
            RECOMMENDATION_PROMPT.format(
                context=context,
                root_cause=root_cause
            )
        )
