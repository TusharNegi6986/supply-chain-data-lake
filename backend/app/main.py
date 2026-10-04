from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .db import fetch_all, fetch_one

app = FastAPI(
    title="Supply Chain Analytics API",
    version="1.0.0"
)

# Allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/kpis")
def get_kpis():
    try:
        return fetch_one("""
            SELECT *
            FROM analytics.supply_chain_kpis
        """)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/monthly-sales")
def get_monthly_sales():
    try:
        return fetch_all("""
            SELECT *
            FROM analytics.monthly_sales
            ORDER BY month
        """)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/categories")
def get_categories():
    try:
        return fetch_all("""
            SELECT *
            FROM analytics.category_performance
        """)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/delivery")
def get_delivery():
    try:
        return fetch_all("""
            SELECT *
            FROM analytics.delivery_performance
        """)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/shipping-modes")
def get_shipping_modes():
    try:
        return fetch_all("""
            SELECT *
            FROM analytics.shipping_mode_performance
        """)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/warehouses")
def get_warehouses():
    try:
        return fetch_all("""
            SELECT *
            FROM analytics.warehouse_inventory_performance
        """)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))