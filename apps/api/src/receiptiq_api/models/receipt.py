from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import Base
from .category import Category
from .line_item import LineItem


class Receipt(Base):
    __tablename__ = "receipts"

    id: Mapped[int] = mapped_column(primary_key=True)
    merchant: Mapped[str]
    purchase_date: Mapped[date]
    total: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"))
    image_key: Mapped[str]
    is_anomaly: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    line_items: Mapped[list[LineItem]] = relationship(
        back_populates="receipt", cascade="all, delete-orphan"
    )
    category: Mapped[Category | None] = relationship()
