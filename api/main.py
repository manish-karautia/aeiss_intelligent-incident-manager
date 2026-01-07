from fastapi import FastAPI
from pydantic import BaseModel
from agents.orchestrator import IncidentOrchestrator

app = FastAPI()
orchestrator = IncidentOrchestrator()

class IncidentRequest(BaseModel):
    text: str

@app.post("/analyze")
def analyze_incident(req: IncidentRequest):
    return orchestrator.run(req.text)
