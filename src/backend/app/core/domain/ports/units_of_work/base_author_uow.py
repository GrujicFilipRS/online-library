from .....shared.domain.ports import BaseUnitOfWork
from ..repositories import BaseAuthorRepository
from ..services import BaseAuthorService


class BaseAuthorUnitOfWork(BaseUnitOfWork):
    author_repo: BaseAuthorRepository
    author_service: BaseAuthorService
