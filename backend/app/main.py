import os
from pathlib import Path
from typing import Optional, List

import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware
from .routers import orders as orders_router, analytics as analytics_router

from .models.order_record import OrderRecord

import re
from app.models import OrderRecord

from app.models.order_record import OrderRecord

from .db import (
    connect,
    disconnect,
    get_orders_from_view,
    get_orders_count,
)

load_dotenv()

REPO_ROOT = Path(__file__).resolve().parents[2]

DEFAULT_CSV = (
    REPO_ROOT
    / "datalake"
    / "raw"
    / "DescriptionDataCoSupplyChain.csv"
)

CSV_PATH = Path(os.getenv("DATA_CSV", str(DEFAULT_CSV)))

app = FastAPI(
    title="Supply Chain DataLake - Backend API",
    version="0.4.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev; tighten in production to your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# remove existing DB endpoint from file (if you already moved it),
# then register routers:
app.include_router(orders_router.router)
app.include_router(analytics_router.router)


# --------------------------------------------------
# Response model for paginated orders
# --------------------------------------------------

class OrdersPage(BaseModel):
    total: int
    count: int
    limit: int
    offset: int
    rows: List[OrderRecord]


# --------------------------------------------------
# Health API
# --------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "ok",
        "csv_path": str(CSV_PATH),
    }


# --------------------------------------------------
# CSV API
# --------------------------------------------------

@app.get("/orders")
def get_orders(
    limit: int = Query(10, ge=1, le=1000),
):
    try:
        df = pd.read_csv(
            CSV_PATH,
            nrows=limit,
        )

        records = df.fillna("").to_dict(
            orient="records"
        )

        return {
            "count": len(records),
            "rows": records,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed reading CSV: {e}",
        )


# --------------------------------------------------
# Database connection lifecycle
# --------------------------------------------------

@app.on_event("startup")
async def startup():
    await connect()


@app.on_event("shutdown")
async def shutdown():
    await disconnect()


# --------------------------------------------------
# Database API
# --------------------------------------------------

def normalize_keys(d: dict) -> dict:
    """Normalize DB keys: remove punctuation, spaces->underscores, lowercase."""
    out = {}
    for k, v in d.items():
        if k is None:
            continue
        s = str(k).strip()
        s = re.sub(r"[^\w\s]", "", s)
        s = re.sub(r"\s+", "_", s)
        s = s.lower()
        out[s] = v
    return out

@app.get("/orders_db")
async def get_orders_db(
    limit: int = Query(10, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    order_by: Optional[str] = None,
):
    try:
        raw_rows = await get_orders_from_view(limit=limit, offset=offset, order_by=order_by)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    typed_rows = []
    for r in raw_rows:
        norm = normalize_keys(r)   # e.g. { "id": 1, "fields": 1, "description": "Type" }
        try:
            rec = OrderRecord.model_validate(norm)   # pydantic v2
            typed_rows.append(rec.model_dump())
        except Exception:
            # fallback: include normalized dict for debugging (so you still see data)
            typed_rows.append(norm)

    total = len(typed_rows)
    return {"total": total, "count": len(typed_rows), "limit": limit, "offset": offset, "rows": typed_rows}