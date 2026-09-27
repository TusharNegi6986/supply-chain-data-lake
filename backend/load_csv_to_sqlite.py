# backend/load_csv_to_sqlite.py  (writes backend/dev.db)
import sqlite3
import pandas as pd
from pathlib import Path

repo_root = Path(__file__).resolve().parents[0]  # backend/
csv_path = repo_root.parent / "datalake" / "raw" / "DescriptionDataCoSupplyChain.csv"
db_path = repo_root / "dev.db"

print("CSV:", csv_path)
print("DB:", db_path)

df = pd.read_csv(csv_path)
df.columns = [c.replace(" ", "_").lower() for c in df.columns]

conn = sqlite3.connect(db_path)
df.to_sql("orders_raw", conn, if_exists="replace", index=False)

with conn:
    conn.execute("DROP VIEW IF EXISTS analytics_order_view")
    conn.execute('''
    CREATE VIEW analytics_order_view AS
    SELECT rowid as id, *
    FROM orders_raw
    ''')
print("Loaded CSV into SQLite and created view analytics_order_view")
conn.close()
