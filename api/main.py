from fastapi import FastAPI
from pydantic import BaseModel
from agents.orchestrator import IncidentOrchestrator

app = FastAPI(
    title="Aegis Intelligent Incident Manager",
    description="Agent-based system for incident understanding, analysis, and recommendation",
    version="1.0.0"
)

orchestrator = IncidentOrchestrator()

class IncidentRequest(BaseModel):
    text: str

class IncidentResponse(BaseModel):
    parsed_incident: dict
    similar_incidents: list
    root_cause: str
    recommended_actions: str

@app.post("/analyze", response_model=IncidentResponse)
def analyze_incident(req: IncidentRequest):
    """
    Analyze an operational incident and return:
    - Structured understanding
    - Similar historical incidents
    - Likely root cause
    - Recommended next best actions
    """
    result = orchestrator.run(req.text)
    return result
