from dataclasses import dataclass
from datetime import datetime
from typing import Self
from uuid import UUID, uuid4

from ..value_objects import ImageURL


@dataclass
class Book:
    book_id: UUID
    title: str
    description: str
    published_year: int
    cover_image_url: ImageURL
    author_id: UUID
    uploaded_by: UUID
    created: datetime

    @classmethod
    def create(
        cls,
        title: str,
        description: str,
        published_year: int,
        cover_image_url: str | None,
        author_id: UUID,
        uploaded_by: UUID,
    ) -> Self:
        return cls(
            book_id=uuid4(),
            title=title,
            description=description,
            published_year=published_year,
            cover_image_url=ImageURL(value=cover_image_url),
            author_id=author_id,
            uploaded_by=uploaded_by,
            created=datetime.now(),
        )
