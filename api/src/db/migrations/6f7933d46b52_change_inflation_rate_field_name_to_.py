"""change inflation rate field name to annual_inflation_rate

Revision ID: 6f7933d46b52
Revises: 30d2f385c777
Create Date: 2025-09-23 14:53:23.093969

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6f7933d46b52'
down_revision: Union[str, Sequence[str], None] = '30d2f385c777'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.alter_column(
        'inflation',
        'inflation_rate',
        new_column_name='annual_inflation_rate',
        existing_type=sa.Float(),
        existing_nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.alter_column(
        'inflation',
        'annual_inflation_rate',
        new_column_name='inflation_rate',
        existing_type=sa.Float(),
        existing_nullable=False,
    )
