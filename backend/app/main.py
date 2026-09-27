import os
from pathlib import Path
from typing import Optional, List

from fastapi import FastAPI, Query, HTTPException
import pandas as pd
from dotenv import load_dotenv

from app.models.order_record import OrderRecord
from app.db import connect, disconnect, get_orders_from_view

load_dotenv()

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CSV = REPO_ROOT / "datalake" / "raw" / "DescriptionDataCoSupplyChain.csv"
CSV_PATH = Path(os.getenv("DATA_CSV", str(DEFAULT_CSV)))

app = FastAPI(title="Supply Chain DataLake - Prototype Backend", version="0.3.0")


# ✅ Health API
@app.get("/health")
def health():
    return {"status": "ok", "csv_path": str(CSV_PATH)}


# ✅ CSV API
@app.get("/orders")
def get_orders(limit: Optional[int] = Query(10, ge=1, le=1000)):
    try:
        df = pd.read_csv(CSV_PATH, nrows=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed reading CSV: {e}")

    records = df.fillna("").to_dict(orient="records")
    return {"count": len(records), "rows": records}


# ✅ DB connection lifecycle
@app.on_event("startup")
async def startup():
    await connect()


@app.on_event("shutdown")
async def shutdown():
    await disconnect()


# ✅ DB API
@app.get("/orders_db", response_model=List[OrderRecord])
async def get_orders_db(
    limit: int = Query(10, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    order_by: Optional[str] = Query(None)
):
    try:
        rows = await get_orders_from_view(
            limit=limit,
            offset=offset,
            order_by=order_by
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return rows