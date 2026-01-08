# agents/sql_agent.py
class SQLAgent:
    def generate_sql(self, question, schema, llm):
        prompt = f"""
You are a senior data analyst.

Schema:
{schema}

Write a SAFE, READ-ONLY SQL query to answer:
"{question}"

Rules:
- Use only SELECT
- No DELETE / UPDATE / DROP
- Return SQL only
"""
        return llm.invoke(prompt).content.strip()
    
        
        sql = sql.replace("```sql", "").replace("```", "").strip()

        return sql
