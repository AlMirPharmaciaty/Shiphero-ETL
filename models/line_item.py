# from datetime import datetime
# from typing import Optional

# from sqlalchemy import String
# from sqlalchemy.orm import Mapped, mapped_column

# from config.database import Base


# class LineItem(Base):
#     "Line items table model"

#     __tablename__ = "line_items"

#     id: Mapped[str] = mapped_column(String(255), primary_key=True)
#     legacy_id: Mapped[int]
#     quantity: Mapped[int]
