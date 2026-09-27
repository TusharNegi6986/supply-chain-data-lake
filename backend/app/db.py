# backend/app/db.py
import os
from typing import List, Dict
from dotenv import load_dotenv
from databases import Database
from sqlalchemy import text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set in .env (backend/.env)")

db = Database(DATABASE_URL)

async def connect():
    await db.connect()

async def disconnect():
    await db.disconnect()

async def get_orders_from_view(limit: int = 10) -> List[Dict]:
    # Replace analytics_order_view with actual view name from docs/API_DATA_CONTRACT.md
    query = text("SELECT * FROM analytics_order_view LIMIT :limit")
    rows = await db.fetch_all(query, values={"limit": limit})
    return [dict(r) for r in rows]