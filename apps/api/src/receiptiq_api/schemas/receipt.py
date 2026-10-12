from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class LineItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    description: str
    quantity: int
    price: Decimal


class ReceiptCreate(BaseModel):
    merchant: str
    purchase_date: date
    total: Decimal
    line_items: list[LineItemOut]


class ReceiptOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    merchant: str
    purchase_date: date
    total: Decimal
    category: str | None = None
    is_anomaly: bool
    created_at: datetime
    line_items: list[LineItemOut]
