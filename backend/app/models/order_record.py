from typing import Optional
from pydantic import BaseModel
import datetime

class OrderRecord(BaseModel):
    order_id: Optional[int] = None
    customer_name: Optional[str] = None
    order_date: Optional[datetime.datetime] = None
    amount: Optional[float] = None
    status: Optional[str] = None