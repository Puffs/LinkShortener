"""create link table

Revision ID: a2018871374f
Revises: 
Create Date: 2026-03-26 14:55:09.192121

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a2018871374f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('links',
    sa.Column('original_link', sa.String(), nullable=False),
    sa.Column('short_link', sa.String(), nullable=False),
    sa.Column('link_count', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('original_link'),
    sa.UniqueConstraint('short_link')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('links')

