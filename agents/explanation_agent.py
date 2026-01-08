# agents/explanation_agent.py
class ExplanationAgent:
    def explain(self, df, llm):
        prompt = f"""
Explain these results for an operations manager:

{df.head(20)}
"""
        return llm.invoke(prompt)
    
