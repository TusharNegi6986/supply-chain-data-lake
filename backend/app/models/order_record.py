from typing import Optional, Any
from pydantic import BaseModel

class OrderRecord(BaseModel):
    id: Optional[int] = None
    fields: Optional[Any] = None
    description: Optional[str] = None
