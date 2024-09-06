from datetime import datetime
from typing import Optional

from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from config.database import Base


class Order(Base):
    "Orders table model"

    __tablename__ = "orders"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    legacy_id: Mapped[Optional[int]]
    order_number: Mapped[Optional[str]] = mapped_column(String(255))
    shop_name: Mapped[Optional[str]] = mapped_column(String(255))
    fulfillment_status: Mapped[Optional[str]] = mapped_column(String(255))
    order_date: Mapped[Optional[datetime]]
    total_tax: Mapped[Optional[float]]
    subtotal: Mapped[Optional[float]]
    total_discounts: Mapped[Optional[float]]
    total_price: Mapped[Optional[float]]
    ready_to_ship: Mapped[Optional[bool]]
    email: Mapped[Optional[str]] = mapped_column(String(255))
    profile: Mapped[Optional[str]] = mapped_column(String(255))
    required_ship_date: Mapped[Optional[datetime]]
    tags = mapped_column(JSON, nullable=True)
    flagged: Mapped[Optional[bool]]
    source: Mapped[Optional[str]] = mapped_column(String(255))
    allow_partial: Mapped[Optional[bool]]
    updated_at: Mapped[Optional[datetime]]
