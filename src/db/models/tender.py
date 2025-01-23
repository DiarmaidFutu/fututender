from datetime import datetime
from sqlalchemy import String, DateTime, Double
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Tender(Base):
    __tablename__ = "tenders"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    publication_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    buyer_name: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str] = mapped_column(String, nullable=False)
    regions: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)
    link: Mapped[str] = mapped_column(String, nullable=False)
    deadline: Mapped[datetime | None] = mapped_column(DateTime)
    amount: Mapped[float | None] = mapped_column(Double)


async def search_tenders(search_string: str): ...
