import sqlite3
from pathlib import Path
db_path = Path(__file__).resolve().parents[1] / "dev.db"  # backend/dev.db
print("DB path:", db_path)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

print("\nTables/views:")
cur.execute("SELECT name, type FROM sqlite_master WHERE type IN ('table','view');")
for r in cur.fetchall():
    print(r)

print("\norders_raw columns:")
cur.execute("PRAGMA table_info('orders_raw')")
print(cur.fetchall())

print("\nanalytics_order_view SQL:")
cur.execute("SELECT sql FROM sqlite_master WHERE type='view' AND name='analytics_order_view'")
print(cur.fetchone())

print("\nOne sample row from the view:")
cur.execute("SELECT * FROM analytics_order_view LIMIT 1")
row = cur.fetchone()
if row:
    cols = [x[1] for x in cur.execute("PRAGMA table_info('orders_raw')")]
    print(dict(zip(cols, row)))
conn.close()
