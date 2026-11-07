"""Create users table.

Revision ID: 0001_create_users
Revises:
Create Date: 2026-11-07
"""

from alembic import op
import sqlalchemy as sa


revision = "0001_create_users"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create the users table."""

    op.create_table(
        "users",
        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "telegram_id",
            sa.BigInteger(),
            nullable=False,
        ),
        sa.Column(
            "username",
            sa.String(length=64),
            nullable=True,
        ),
        sa.Column(
            "first_name",
            sa.String(length=128),
            nullable=False,
        ),
        sa.Column(
            "language",
            sa.String(length=10),
            nullable=False,
            server_default="uz",
        ),
        sa.Column(
            "country",
            sa.String(length=100),
            nullable=True,
        ),
        sa.Column(
            "city",
            sa.String(length=100),
            nullable=True,
        ),
        sa.Column(
            "timezone",
            sa.String(length=64),
            nullable=False,
            server_default="UTC",
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
        sa.Column(
            "last_seen_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )

    op.create_index(
        "ix_users_telegram_id",
        "users",
        ["telegram_id"],
        unique=True,
    )


def downgrade() -> None:
    """Remove the users table."""

    op.drop_index(
        "ix_users_telegram_id",
        table_name="users",
    )

    op.drop_table("users")
