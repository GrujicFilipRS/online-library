from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import UUID as UUID_ORM

from ....shared.utils import Base


class DBUser(Base):
    __tablename__ = "users"

    user_id: Mapped[UUID] = mapped_column(
        UUID_ORM(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    username: Mapped[str] = mapped_column(
        String(73),
        nullable=False,
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=True,  # Nullable because of possible Oauth registration
    )
    role: Mapped[str] = mapped_column(
        String(),
        nullable=False,
        default="User",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now,
    )
