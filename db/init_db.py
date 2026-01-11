import duckdb
from pathlib import Path

# Ensure correct path regardless of where script is run
BASE_DIR = Path(__file__).resolve().parents[1]
CSV_PATH = BASE_DIR / "data" / "incident_logs.csv"
DB_PATH = BASE_DIR / "incidents.duckdb"

con = duckdb.connect(str(DB_PATH))

con.execute("""
CREATE OR REPLACE TABLE incidents AS
SELECT * FROM read_csv_auto(?)
""", [str(CSV_PATH)])

print("✅ Database initialized successfully")
print("📦 Database file:", DB_PATH)
print("📄 Source CSV:", CSV_PATH)
