from uuid import UUID, uuid4

from sqlalchemy import UUID as UUID_ORM
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ....shared.utils import Base


class DBAuthor(Base):
    __tablename__ = "authors"

    author_id: Mapped[UUID] = mapped_column(
        UUID_ORM(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    nationality: Mapped[str] = mapped_column(String(255), nullable=False)
    image_url: Mapped[str] = mapped_column(String(255), nullable=False)
