from datetime import datetime
from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from config.database import Base


class Shipment(Base):
    "Shipments table model"

    __tablename__ = "shipments"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    legacy_id: Mapped[Optional[int]]
    order_id: Mapped[Optional[str]] = mapped_column(String(255))
    user_id: Mapped[Optional[str]] = mapped_column(String(255))
    warehouse_id: Mapped[Optional[str]] = mapped_column(String(255))
    pending_shipment_id: Mapped[Optional[str]] = mapped_column(String(255))
    profile: Mapped[Optional[str]] = mapped_column(String(255))
    picked_up: Mapped[Optional[bool]]
    completed: Mapped[Optional[bool]]
    created_date: Mapped[Optional[datetime]]
    total_packages: Mapped[Optional[int]]
