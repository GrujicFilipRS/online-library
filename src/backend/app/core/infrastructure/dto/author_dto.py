from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AuthorDTO(BaseModel):
    author_id: UUID
    name: str
    nationality: str
    image_url: str | None

    model_config = ConfigDict(
        from_attributes=True, frozen=True, str_strip_whitespace=True
    )
