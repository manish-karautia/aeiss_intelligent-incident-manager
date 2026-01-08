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

@app.post("/analyze")
def analyze_incident(req: IncidentRequest):
    """
    Analyze incident or execute SQL-based analytics depending on intent.
    
    """
    result = orchestrator.run(req.text)
    return result
