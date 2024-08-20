from sqlalchemy import Column, String, DateTime, Float
from sqlalchemy.sql import func

from config.database import Base


class Order(Base):
    "Orders table model"

    __tablename__ = "orders"

    id = Column(String, primary_key=True)
    order_number = Column(String)
    partner_order_id = Column(String)
    status = Column(String)
    source = Column(String)
    shop_name = Column(String)
    total_price = Column(Float)
    created_at = Column(DateTime)
    shipped_at = Column(DateTime)
    created_by = Column(String)
    shipped_by = Column(String)
    fulfillment_time = Column(String)
    fulfillment_time_secs = Column(Float)
    extracted_at = Column(DateTime)
    transformed_at = Column(DateTime)
    loaded_at = Column(DateTime, default=func.now())
