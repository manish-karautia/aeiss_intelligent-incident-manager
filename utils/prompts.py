INCIDENT_PARSE_PROMPT = """
Extract the following as JSON:
- service
- region
- severity
- symptoms
- time_context

Incident:
{text}
"""

ROOT_CAUSE_PROMPT = """
You are an SRE expert.
Analyze the incident context and infer the most likely root cause.
Explain your reasoning clearly.

Context:
{context}
"""

RECOMMENDATION_PROMPT = """
Recommend next best actions ranked by priority.
Include confidence score (0-1) and reasoning.

Context:
{context}
Root Cause:
{root_cause}
"""
