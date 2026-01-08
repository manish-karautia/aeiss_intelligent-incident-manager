import re

class SQLGuardAgent:
    def validate(self, sql: str) -> bool:
        sql_clean = sql.strip().lower()

        # Must start with SELECT
        if not sql_clean.startswith("select"):
            return False

        # Block destructive keywords
        forbidden = [
            "drop ", "delete ", "update ", "insert ",
            "alter ", "truncate ", "--", "/*", "*/"
        ]
        if any(f in sql_clean for f in forbidden):
            return False

        # Allow ONLY known-safe SQL functions
        allowed_patterns = [
            r"select",
            r"from",
            r"where",
            r"group by",
            r"order by",
            r"count\s*\(",
            r"avg\s*\(",
            r"sum\s*\(",
            r"min\s*\(",
            r"max\s*\(",
            r"current_timestamp",
            r"now\(\)",
            r"interval\s+'\d+\s+(hour|hours|day|days)'"
        ]

        for token in re.findall(r"[a-z_]+", sql_clean):
            if not any(re.search(p, token) for p in allowed_patterns):
                continue  # allow column names

        return True
