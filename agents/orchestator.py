from agents.nlp_agent import NLPAgent
from agents.retrieval_agent import RetrievalAgent
from agents.context_agent import ContextAgent
from agents.analysis_agent import AnalysisAgent
from agents.recommendation_agent import RecommendationAgent

class IncidentOrchestrator:
    def __init__(self):
        self.nlp = NLPAgent()
        self.retriever = RetrievalAgent()
        self.context = ContextAgent()
        self.analysis = AnalysisAgent()
        self.recommendation = RecommendationAgent()

    def run(self, text):
        parsed = self.nlp.run(text)
        history = self.retriever.run(text)
        ctx = self.context.build(parsed, history)
        root = self.analysis.run(ctx)
        actions = self.recommendation.run(ctx, root)

        return {
            "parsed_incident": parsed,
            "similar_incidents": history,
            "root_cause": root,
            "recommended_actions": actions
        }
