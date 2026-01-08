# db/init_db.py
import duckdb

con = duckdb.connect("incidents.duckdb")

con.execute("""
CREATE TABLE incidents AS
SELECT * FROM read_csv_auto('data/incident_logs.csv')
""")

