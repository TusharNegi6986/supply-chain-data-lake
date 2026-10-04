import os
import asyncio
import logging
from typing import Optional

from databases import Database
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("backend.db")

if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    )
    logger.addHandler(handler)

logger.setLevel(logging.INFO)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite+aiosqlite:///./dev.db"
)

database = Database(DATABASE_URL)

_resolved_view_name: Optional[str] = None


def using_sqlite() -> bool:
    return DATABASE_URL.startswith("sqlite")


async def connect(retries: int = 8, delay: float = 1.0):
    """
    Connect to database with retry/backoff.
    """
    if database.is_connected:
        return

    last_exc = None
    backoff = delay

    for attempt in range(retries):
        try:
            logger.info(
                "DB connect attempt %s/%s",
                attempt + 1,
                retries
            )

            await database.connect()
            logger.info("DB connected")
            return

        except Exception as exc:
            last_exc = exc
            logger.warning(
                "DB connect attempt %s failed: %r",
                attempt + 1,
                exc
            )

            if attempt < retries - 1:
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, 8.0)

    logger.error("All DB connection attempts failed.")

    if last_exc:
        raise last_exc

    raise RuntimeError("Database connection failed")


async def disconnect():
    if database.is_connected:
        await database.disconnect()
        logger.info("DB disconnected")


# ✅ NEW FUNCTION ADDED (your retry helper)
async def try_connect_with_retry(retries=10, delay=1.0):
    import asyncio

    db = globals().get("database")

    if db is None:
        db = globals().get("db")

    if db is None:
        raise RuntimeError("Database object was not found in app.db")

    last_error = None

    for attempt in range(1, retries + 1):
        try:
            if not db.is_connected:
                await db.connect()

            print(f"DB connected on attempt {attempt}")
            return

        except Exception as exc:
            last_error = exc
            print(f"DB connect attempt {attempt}/{retries} failed: {exc}")

            if attempt < retries:
                await asyncio.sleep(delay)

    raise last_error


async def resolve_view_name() -> str:
    """
    Resolve analytics view depending on database type.
    """
    global _resolved_view_name

    if _resolved_view_name:
        return _resolved_view_name

    if using_sqlite():
        candidates = [
            "analytics_order_view"
        ]
    else:
        candidates = [
            "analytics.analytics_order_view",
            "public.analytics_order_view"
        ]

    for name in candidates:
        try:
            query = f"SELECT 1 FROM {name} LIMIT 1"
            await database.fetch_one(query)

            _resolved_view_name = name
            logger.info("Using analytics view: %s", name)
            return name

        except Exception as exc:
            logger.warning(
                "View %s not available: %r",
                name,
                exc
            )

    raise RuntimeError(
        "analytics_order_view not found. "
        "Make sure analytics_views.sql has been applied."
    )


async def get_orders_count() -> int:
    view = await resolve_view_name()

    query = f"""
        SELECT COUNT(*) AS cnt
        FROM {view}
    """

    row = await database.fetch_one(query)

    if row is None:
        return 0

    return int(row["cnt"])


async def get_orders_from_view(
    limit: int = 10,
    offset: int = 0,
    order_by: Optional[str] = None
):
    view = await resolve_view_name()

    limit = max(1, min(int(limit), 1000))
    offset = max(0, int(offset))

    allowed_order_cols = {
        "id",
        "fields",
        "description"
    }

    order_clause = ""
    if order_by:
        column = order_by.strip().lower()
        if column in allowed_order_cols:
            order_clause = f" ORDER BY {column}"

    query = (
        f"SELECT * FROM {view}"
        f"{order_clause}"
        f" LIMIT :limit OFFSET :offset"
    )

    rows = await database.fetch_all(
        query=query,
        values={
            "limit": limit,
            "offset": offset
        }
    )

    total = await get_orders_count()

    rows_out = [
        dict(row)
        for row in rows
    ]

    return {
        "total": total,
        "count": len(rows_out),
        "limit": limit,
        "offset": offset,
        "rows": rows_out
    }