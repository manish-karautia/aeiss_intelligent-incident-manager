# agents/schema_agent.py
class SchemaAgent:
    def get_schema(self, con):
        rows = con.execute("DESCRIBE incidents").fetchall()
        return "\n".join([f"{r[0]} ({r[1]})" for r in rows])
