import os
from typing import List, Dict, Optional

from dotenv import load_dotenv
from databases import Database

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL not set in .env (backend/.env)"
    )

db = Database(DATABASE_URL)


async def connect():
    await db.connect()


async def disconnect():
    await db.disconnect()


async def get_orders_from_view(
    limit: int = 10,
    offset: int = 0,
    order_by: Optional[str] = None,
) -> List[Dict]:

    limit = int(limit)
    offset = int(offset)

    allowed_order_cols = {
        "id",
    }

    order_clause = ""

    if order_by:
        col = order_by.strip().lower()

        if col in allowed_order_cols:
            order_clause = f" ORDER BY {col}"

    query = (
        f"SELECT * FROM analytics_order_view"
        f"{order_clause}"
        f" LIMIT {limit} OFFSET {offset}"
    )

    rows = await db.fetch_all(query)

    return [dict(row) for row in rows]


async def get_orders_count() -> int:
    query = "SELECT COUNT(*) AS cnt FROM analytics_order_view"

    row = await db.fetch_one(query)

    if row is None:
        return 0

    return int(row["cnt"])