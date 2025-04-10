import datetime

from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class Secret(Base):
    __tablename__ = "secrets"

    key: Mapped[str] = mapped_column(primary_key=True, index=True)
    secret: Mapped[str] = mapped_column(nullable=False)
    passphrase: Mapped[str | None]
    ttl_seconds: Mapped[int] = mapped_column(default=300)
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    was_read: Mapped[bool] = mapped_column(default=False)

    logs = relationship(
        "SecretLog",
        back_populates="secret",
        cascade="all, delete-orphan",
    )


class SecretLog(Base):
    __tablename__ = "secret_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    ip_address: Mapped[str]
    action: Mapped[str]
    secret_key: Mapped[str | None] = mapped_column(
        ForeignKey("secrets.key", ondelete="SET NULL")
    )
    timestamp: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )

    secret = relationship("Secret", back_populates="logs")
