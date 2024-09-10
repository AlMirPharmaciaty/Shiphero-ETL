from typing import Optional

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from config.database import Base


class Warehouse(Base):
    "Warehouse table model"

    __tablename__ = "warehouses"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    legacy_id: Mapped[Optional[int]]
    identifier: Mapped[Optional[str]] = mapped_column(String(255))
    profile: Mapped[Optional[str]] = mapped_column(String(255))
    company_alias: Mapped[Optional[str]] = mapped_column(String(255))
    name: Mapped[Optional[str]] = mapped_column(String(255))
    address1: Mapped[Optional[str]] = mapped_column(Text)
    address2: Mapped[Optional[str]] = mapped_column(Text)
    city: Mapped[Optional[str]] = mapped_column(String(255))
    country: Mapped[Optional[str]] = mapped_column(String(255))
