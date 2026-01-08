class ContextAgent:
    def build(self, parsed_incident, historical_incidents):
        actions = [
            i.get("action_taken", "unknown")
            for i in historical_incidents
        ]
        metrics = [
            i.get("metric_type", "unknown")
            for i in historical_incidents
        ]

        return {
            "current_incident": parsed_incident,
            "historical_incidents": historical_incidents,
            "frequent_actions": list(set(actions)),
            "frequent_metrics": list(set(metrics))
        }
