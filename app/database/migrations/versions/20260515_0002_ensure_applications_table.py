"""ensure applications table exists"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "20260515_0002"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "applications" not in inspector.get_table_names():
        op.create_table(
            "applications",
            sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
            sa.Column("full_name", sa.String(length=255), nullable=False),
            sa.Column("age", sa.Integer(), nullable=False),
            sa.Column("city", sa.String(length=255), nullable=False),
            sa.Column("target_weight_loss", sa.Integer(), nullable=False),
            sa.Column("phone", sa.String(length=32), nullable=False),
            sa.Column("telegram_username", sa.String(length=255), nullable=True),
            sa.Column("telegram_id", sa.BigInteger(), nullable=False),
            sa.Column(
                "created_at",
                sa.DateTime(timezone=False),
                nullable=False,
                server_default=sa.text("CURRENT_TIMESTAMP"),
            ),
        )

    inspector = sa.inspect(bind)
    indexes = {index["name"] for index in inspector.get_indexes("applications")}
    if "ix_applications_telegram_id" not in indexes:
        op.create_index(
            "ix_applications_telegram_id",
            "applications",
            ["telegram_id"],
            unique=False,
        )


def downgrade() -> None:
    pass
