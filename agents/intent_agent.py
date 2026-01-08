# agents/intent_agent.py
class IntentAgent:
    def classify(self, text, llm):
        prompt = """
Classify the user request into EXACTLY one category.

Rules:
- If the request asks for counts, averages, trends, metrics, reports → SQL_ANALYSIS
- If it asks "why", "cause", "issue", "reason" → INCIDENT_REASONING
- If it asks "what should we do" → ACTION_RECOMMENDATION

Return ONLY ONE WORD from:
SQL_ANALYSIS
INCIDENT_REASONING
ACTION_RECOMMENDATION

User request:
"""
        response = llm.invoke(prompt + text)
        return response.strip()

