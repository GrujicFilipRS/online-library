from ...domain.models import Author
from ..db_models import DBAuthor
from ..dto import AuthorDTO


class AuthorMapper:
    @staticmethod
    def to_domain(db_author: DBAuthor) -> Author:
        return Author(
            author_id=db_author.author_id,
            name=db_author.name,
            nationality=db_author.nationality,
            image_url=db_author.image_url,
        )

    @staticmethod
    def to_orm(author: Author) -> DBAuthor:
        return DBAuthor(
            author_id=author.author_id,
            name=author.name,
            nationality=author.nationality,
            image_url=author.image_url,
        )

    @staticmethod
    def to_dto(author: Author) -> AuthorDTO:
        return AuthorDTO(
            author_id=author.author_id,
            name=author.name,
            nationality=author.nationality,
            image_url=author.image_url,
        )
