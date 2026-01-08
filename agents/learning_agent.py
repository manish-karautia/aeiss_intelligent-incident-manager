import json
import os

class LearningAgent:
    def learn(self, incident, resolution):
        path = "memory/success_stats.json"

        if not os.path.exists(path):
            with open(path, "w") as f:
                json.dump({}, f)

        with open(path, "r+") as f:
            stats = json.load(f)
            action = resolution.get("action", "unknown")
            stats[action] = stats.get(action, 0) + 1
            f.seek(0)
            json.dump(stats, f, indent=2)
