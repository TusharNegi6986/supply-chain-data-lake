import os
from typing import List, Dict, Optional
from dotenv import load_dotenv
from databases import Database

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set in .env (backend/.env)")

db = Database(DATABASE_URL)

async def connect():
    await db.connect()

async def disconnect():
    await db.disconnect()

async def get_orders_from_view(limit: int = 10, offset: int = 0, order_by: Optional[str] = None) -> List[Dict]:
    """
    Returns rows from analytics_order_view with basic pagination and ordering.
    WARNING: order_by is used only to specify a column name; in production validate allowed columns.
    """
    limit = int(limit)
    offset = int(offset)
    # Basic whitelist for ordering to avoid SQL injection. Add CSV/view columns as needed.
    allowed_order_cols = {"id", "rowid"}  # extend this with actual column names from your CSV/view
    order_clause = ""
    if order_by:
        col = order_by.strip().lower()
        if col in allowed_order_cols:
            order_clause = f" ORDER BY {col} "
    query = f"SELECT * FROM analytics_order_view{order_clause} LIMIT {limit} OFFSET {offset}"
    rows = await db.fetch_all(query)
    return [dict(r) for r in rows]
