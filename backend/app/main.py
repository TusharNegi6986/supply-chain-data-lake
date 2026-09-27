import os
from pathlib import Path
from typing import Optional, List

import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel

from .models.order_record import OrderRecord
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

@app.get(
    "/orders_db",
    response_model=OrdersPage,
)
async def get_orders_db(
    limit: int = Query(
        10,
        ge=1,
        le=1000,
    ),
    offset: int = Query(
        0,
        ge=0,
    ),
    order_by: Optional[str] = Query(
        None,
        description="Column name to order by",
    ),
):
    try:
        rows = await get_orders_from_view(
            limit=limit,
            offset=offset,
            order_by=order_by,
        )

        total = await get_orders_count()

        return {
            "total": total,
            "count": len(rows),
            "limit": limit,
            "offset": offset,
            "rows": rows,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )