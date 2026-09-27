import sqlite3, os
repo = r"C:\Users\uditv\Projects\supply-chain-data-lake"
paths = [os.path.join(repo,"dev.db"), os.path.join(repo,"backend","dev.db")]
for p in paths:
    print("Checking:", p)
    if not os.path.exists(p):
        print("  -> not found")
        continue
    conn = sqlite3.connect(p)
    cur = conn.cursor()
    cur.execute("SELECT name, type FROM sqlite_master WHERE type IN ('table','view');")
    rows = cur.fetchall()
    print("  tables/views:", rows)
    conn.close()
