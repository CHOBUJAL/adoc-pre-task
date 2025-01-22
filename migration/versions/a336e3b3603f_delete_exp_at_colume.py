"""delete exp_at colume

Revision ID: a336e3b3603f
Revises: b7e0f17e3c0b
Create Date: 2025-01-22 19:54:34.313264

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'a336e3b3603f'
down_revision: Union[str, None] = 'b7e0f17e3c0b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('refresh_tokens', 'expires_at')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('refresh_tokens', sa.Column('expires_at', mysql.DATETIME(), nullable=False, comment='레코드가 생성된 시간 in UTC'))
    # ### end Alembic commands ###
