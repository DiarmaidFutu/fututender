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
