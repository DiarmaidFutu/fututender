import traceback

from db.models.tenderdbo import (
    TenderDbo,
    save_tender_dbo,
    save_tender_dbos,
    get_tender_dbos,
)
from exceptions.database_exception import FutuTenderDatabaseException
from .base import Base
from typing import Annotated
from datetime import datetime


class Tender(Base):
    id: Annotated[
        str, "This is the publication notice id/ND field (seems to be the same)"
    ]
    publication_date: Annotated[datetime, "The time the tender was published"]
    buyer_name: str
    country: str
    regions: list[str]
    title: str
    type: Annotated[
        str, "We get the type from the contract nature -e.g. supplies, services, etc"
    ]
    link: str
    deadline: datetime | None = None
    amount: float | None = None
    currency: str | None = None


async def save_tender(tender: Tender) -> Tender:
    tender_dbo = TenderDbo(**tender.model_dump())
    tender_dbo = await save_tender_dbo(tender_dbo)
    return Tender(**tender_dbo.__dict__)


async def save_tenders(tenders: list[Tender]) -> list[Tender]:
    tender_dbos = [TenderDbo(**tender.model_dump()) for tender in tenders]
    tender_dbos = await save_tender_dbos(tender_dbos)
    return [Tender(**tender_dbo.__dict__) for tender_dbo in tender_dbos]


async def get_tenders() -> list[Tender]:
    try:
        tender_dbos = await get_tender_dbos()
    except Exception as e:
        print(e)
        print(traceback.print_exc())
        raise FutuTenderDatabaseException from e
    return [Tender(**tender_dbo.__dict__) for tender_dbo in tender_dbos]
