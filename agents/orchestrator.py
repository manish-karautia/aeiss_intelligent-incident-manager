import duckdb

# Existing agents (keep)
from agents.nlp_agent import NLPAgent
from agents.retrieval_agent import RetrievalAgent
from agents.context_agent import ContextAgent
from agents.analysis_agent import AnalysisAgent
from agents.recommendation_agent import RecommendationAgent

# NEW agents
from agents.intent_agent import IntentAgent
from agents.schema_agent import SchemaAgent
from agents.sql_agent import SQLAgent
from agents.sql_guard_agent import SQLGuardAgent
from agents.sql_executor_agent import SQLExecutorAgent
from agents.explanation_agent import ExplanationAgent

# LLM router
from agents.llm_router import LLMRouter

from utils.text_normalizer import normalize_time_phrases

class IncidentOrchestrator:
    def __init__(self):
        # ---- Existing pipeline ----
        self.nlp = NLPAgent()
        self.retriever = RetrievalAgent()
        self.context = ContextAgent()
        self.analysis = AnalysisAgent()
        self.recommendation = RecommendationAgent()

        # ---- New SQL pipeline ----
        self.intent_agent = IntentAgent()
        self.schema_agent = SchemaAgent()
        self.sql_agent = SQLAgent()
        self.sql_guard = SQLGuardAgent()
        self.sql_executor = SQLExecutorAgent()
        self.explainer = ExplanationAgent()
        self.llm_router = LLMRouter()

        # Database connection (DuckDB)
        self.con = duckdb.connect("incidents.duckdb", read_only=False)

    def run(self, text: str):
        """
        Main brain of the system
        Decides: SQL analysis OR incident reasoning
        """
        
        text = normalize_time_phrases(text)


        # 1️⃣ Decide intent
        llm = self.llm_router.get_llm("intent")
        intent = self.intent_agent.classify(text, llm)

        # ============================
        # 🟦 SQL / CSV / METRICS PATH
        # ============================
        if intent == "SQL_ANALYSIS":
            sql_llm = self.llm_router.get_llm("sql")

            schema = self.schema_agent.get_schema(self.con)
            sql = self.sql_agent.generate_sql(text, schema, sql_llm)
            


            if not self.sql_guard.validate(sql):
                return {"error": "Unsafe SQL generated"}

            df = self.sql_executor.run(self.con, sql)
            explanation = self.explainer.explain(df, sql_llm)

            return {
                "intent": "SQL_ANALYSIS",
                "generated_sql": sql,
                "data": df.to_dict(orient="records"),
                "explanation": explanation
            }

        # ============================
        # 🟩 INCIDENT / RAG PATH
        # ============================
        parsed = self.nlp.run(text)
        history = self.retriever.run(text)
        ctx = self.context.build(parsed, history)
        root = self.analysis.run(ctx)
        actions = self.recommendation.run(ctx, root)

        return {
            "intent": "INCIDENT_REASONING",
            "parsed_incident": parsed,
            "similar_incidents": history,
            "root_cause": root,
            "recommended_actions": actions
        }
