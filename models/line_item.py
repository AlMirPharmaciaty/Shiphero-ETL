from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from config.database import Base


class LineItem(Base):
    "Line items table model"

    __tablename__ = "line_items"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    legacy_id: Mapped[Optional[int]]
    order_id: Mapped[Optional[str]] = mapped_column(String(255))
    sku: Mapped[Optional[str]] = mapped_column(String(255))
    quantity: Mapped[Optional[int]]
    product_name: Mapped[Optional[str]] = mapped_column(String(255))
    price: Mapped[Optional[float]]
    subtotal: Mapped[Optional[float]]
    quantity_allocated: Mapped[Optional[int]]
