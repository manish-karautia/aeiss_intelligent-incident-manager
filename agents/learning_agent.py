import json

class LearningAgent:
    def learn(self, incident, resolution):
        with open("memory/success_stats.json", "r+") as f:
            stats = json.load(f)
            action = resolution["action"]
            stats[action] = stats.get(action, 0) + 1
            f.seek(0)
            json.dump(stats, f, indent=2)
