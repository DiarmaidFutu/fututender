"""Changed to use ARRAY type in database

Revision ID: 686a95d4755c
Revises: 42ccf5b36691
Create Date: 2025-01-23 12:08:22.076921

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '686a95d4755c'
down_revision: Union[str, None] = '42ccf5b36691'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
