"""add user nickname

Revision ID: 002_add_user_nickname
Revises: 001_initial
Create Date: 2026-05-07

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "002_add_user_nickname"
down_revision: Union[str, Sequence[str], None] = "001_initial"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("nickname", sa.String(length=64), nullable=True))
    op.create_index("ix_users_nickname", "users", ["nickname"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_users_nickname", table_name="users")
    op.drop_column("users", "nickname")

