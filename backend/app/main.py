import os
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Query, HTTPException
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CSV = REPO_ROOT / "datalake" / "raw" / "DescriptionDataCoSupplyChain.csv"
CSV_PATH = Path(os.getenv("DATA_CSV", str(DEFAULT_CSV)))

app = FastAPI(title="Supply Chain DataLake - Prototype Backend", version="0.3.0")

# CSV prototype
@app.get("/health")
def health():
    return {"status": "ok", "csv_path": str(CSV_PATH)}

@app.get("/orders")
def get_orders(limit: Optional[int] = Query(10, ge=1, le=1000)):
    try:
        df = pd.read_csv(CSV_PATH, nrows=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed reading CSV: {e}")
    records = df.fillna("").to_dict(orient="records")
    return {"count": len(records), "rows": records}

# DB integration (async)
import asyncio
from .db import connect, disconnect, get_orders_from_view

@app.on_event("startup")
async def startup():
    await connect()

@app.on_event("shutdown")
async def shutdown():
    await disconnect()

@app.get("/orders_db")
async def get_orders_db(
    limit: int = Query(10, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    order_by: Optional[str] = Query(None, description="Column name to order by (whitelisted)"),
):
    try:
        rows = await get_orders_from_view(limit=limit, offset=offset, order_by=order_by)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"count": len(rows), "rows": rows}
