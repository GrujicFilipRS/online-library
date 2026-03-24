from typing import Self
from uuid import UUID, uuid4


class Author:
    def __init__(
        self, author_id: UUID, name: str, nationality: str, image_url: str
    ) -> None:
        self.author_id = author_id
        self.name = name
        self.nationality = nationality
        self.image_url = image_url
        return

    @classmethod
    def create(cls, name: str, nationality: str, image_url: str) -> Self:
        author_id = uuid4()
        return cls(
            author_id,
            name,
            nationality,
            image_url,
        )
