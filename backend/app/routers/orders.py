# backend/app/routers/orders.py
from typing import Optional
from fastapi import APIRouter, Query, HTTPException
from typing import List
from ..db import get_orders_from_view, get_orders_count
from ..models.order_record import OrderRecord

router = APIRouter(prefix="/orders", tags=["orders"])

@router.get("/db", response_model=dict)
async def list_orders_db(
    limit: int = Query(10, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    order_by: Optional[str] = Query(None),
    customer_name: Optional[str] = Query(None, description="filter by customer name"),
    date_from: Optional[str] = Query(None, description="YYYY-MM-DD"),
    date_to: Optional[str] = Query(None, description="YYYY-MM-DD"),
):
    """
    Returns page of orders from analytics_order_view with simple filters.
    The SQL for filtering should be added to app.db.get_orders_from_view.
    """
    try:
        rows = await get_orders_from_view(
            limit=limit, offset=offset, order_by=order_by
            # TODO: extend get_orders_from_view signature to accept filters (customer_name, date_from, date_to)
        )
        total = await get_orders_count()
        return {"total": total, "count": len(rows), "limit": limit, "offset": offset, "rows": rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))