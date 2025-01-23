from collections.abc import Iterable
from datetime import datetime

from sqlalchemy import String, DateTime, Double, select
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from ..database_session_manager import db_session_context, AsyncSession


class TenderDbo(Base):
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


async def save_tender_dbo(tender_dbo: TenderDbo) -> TenderDbo:
    session: AsyncSession = db_session_context.get()
    session.add(tender_dbo)
    await session.commit()
    await session.refresh(tender_dbo)
    return tender_dbo


async def save_tender_dbos(tender_dbos: list[TenderDbo]) -> list[TenderDbo]:
    session: AsyncSession = db_session_context.get()
    for tender_dbo in tender_dbos:
        session.add(tender_dbo)
    await session.commit()
    await session.refresh(tender_dbos)
    return tender_dbos


async def get_tender_dbo(id: str) -> TenderDbo | None:
    session: AsyncSession = db_session_context.get()
    query = select(TenderDbo).where(TenderDbo.id == id)
    result = await session.scalar(query)
    return result


async def get_tender_dbos(ids: list[str] | None = None) -> Iterable[TenderDbo]:
    session: AsyncSession = db_session_context.get()
    query = select(TenderDbo)
    if ids is not None:
        query = query.where(TenderDbo.id.in_(ids))
    results = await session.scalars(query)
    return results.all()
