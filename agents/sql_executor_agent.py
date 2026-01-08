# agents/sql_executor_agent.py
class SQLExecutorAgent:
    def run(self, con, sql):
        return con.execute(sql).fetchdf()
