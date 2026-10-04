# backend/app/main.py
import os
import logging
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from . import db as db_module
from app import db as db_module

logger = logging.getLogger("backend.main")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.addHandler(handler)

app = FastAPI(title="Supply Chain Backend (FastAPI)")

class OrdersResponse(BaseModel):
    total: int
    count: int
    limit: int
    offset: int
    rows: list


@app.on_event("startup")
async def startup_event():
    # Connect with retries to give Docker Postgres time to be ready.
    try:
        await db_module.try_connect_with_retry(retries=10, delay=1.0)
        # Resolve view now so errors are visible in logs early.
        try:
            await db_module.resolve_view_name()
        except Exception as exc:
            logger.error(f"View resolution failed during startup: {exc!r}")
            # Do NOT crash — let endpoints report error; but log clearly.
    except Exception as exc:
        raise


@app.on_event("shutdown")
async def shutdown_event():
    await db_module.disconnect()


@app.get("/health")
async def health():
    """
    Returns basic health and which DATABASE_URL is in use.
    """
    return {"status": "ok", "database_url": os.environ.get("DATABASE_URL", "sqlite+aiosqlite:///./dev.db")}


@app.get("/orders_db", response_model=OrdersResponse)
async def orders_db(limit: int = Query(10, ge=1, le=100), offset: int = Query(0, ge=0)):
    """
    Return rows from analytics view with pagination.
    Tries to auto-detect view name (analytics.analytics_order_view or analytics_order_view).
    """
    try:
        result = await db_module.get_orders_from_view(limit=limit, offset=offset)
        return result
    except RuntimeError as exc:
        # Clear error when view missing
        raise HTTPException(status_code=500, detail=str(exc))
    except Exception as exc:
        logger.exception("Unexpected error while fetching orders")
        raise HTTPException(status_code=500, detail="unexpected server error")