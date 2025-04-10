"""Create all tables

Revision ID: 41edce534a09
Revises:
Create Date: 2025-04-10 10:34:31.537553

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "41edce534a09"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "secrets",
        sa.Column("key", sa.String(), nullable=False),
        sa.Column("secret", sa.String(), nullable=False),
        sa.Column("passphrase", sa.String(), nullable=True),
        sa.Column("ttl_seconds", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column("was_read", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("key"),
    )
    op.create_index(op.f("ix_secrets_key"), "secrets", ["key"], unique=False)
    op.create_table(
        "secret_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("ip_address", sa.String(), nullable=False),
        sa.Column("action", sa.String(), nullable=False),
        sa.Column("secret_key", sa.String(), nullable=True),
        sa.Column(
            "timestamp",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["secret_key"], ["secrets.key"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_secret_logs_id"), "secret_logs", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_secret_logs_id"), table_name="secret_logs")
    op.drop_table("secret_logs")
    op.drop_index(op.f("ix_secrets_key"), table_name="secrets")
    op.drop_table("secrets")
    # ### end Alembic commands ###
