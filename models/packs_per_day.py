from datetime import datetime
from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from config.database import Base


class PacksPerDay(Base):
    "Packs per day table model"

    __tablename__ = "packs_per_day"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    legacy_id: Mapped[Optional[int]]
    order_id: Mapped[Optional[str]] = mapped_column(String(255))
    warehouse_id: Mapped[Optional[str]] = mapped_column(String(255))
    shipment_id: Mapped[Optional[str]] = mapped_column(String(255))
    user_id: Mapped[Optional[str]] = mapped_column(String(255))
    user_first_name: Mapped[Optional[str]] = mapped_column(String(255))
    user_last_name: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime]]
