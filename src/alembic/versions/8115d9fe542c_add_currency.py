"""Add currency

Revision ID: 8115d9fe542c
Revises: 686a95d4755c
Create Date: 2025-01-23 12:57:56.277346

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8115d9fe542c'
down_revision: Union[str, None] = '686a95d4755c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tenders', sa.Column('currency', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tenders', 'currency')
    # ### end Alembic commands ###
