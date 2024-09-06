from datetime import datetime
from typing import Optional

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from config.database import Base


class OrderHistory(Base):
    "Order History table model"

    __tablename__ = "order_history"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    order_id: Mapped[Optional[str]] = mapped_column(String(255))
    user_id: Mapped[Optional[str]] = mapped_column(String(255))
    account_id: Mapped[Optional[str]] = mapped_column(String(255))
    username: Mapped[Optional[str]] = mapped_column(String(255))
    order_number: Mapped[Optional[str]] = mapped_column(String(255))
    information: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime]]
