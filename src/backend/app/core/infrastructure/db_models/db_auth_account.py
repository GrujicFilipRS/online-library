from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import UUID as UUID_ORM
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from ....shared.utils import Base


class DBAuthAccount(Base):
    __tablename__ = "auth_accounts"

    auth_account_id: Mapped[UUID] = mapped_column(
        UUID_ORM(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.user_id"),
        nullable=False,
    )
    provider: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    provider_user_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now,
    )
