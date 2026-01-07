class ContextAgent:
    def build(self, parsed_incident, historical_incidents):
        actions = [i["action_taken"] for i in historical_incidents]
        metrics = [i["metric_type"] for i in historical_incidents]

        return {
            "current_incident": parsed_incident,
            "historical_incidents": historical_incidents,
            "frequent_actions": list(set(actions)),
            "frequent_metrics": list(set(metrics))
        }
