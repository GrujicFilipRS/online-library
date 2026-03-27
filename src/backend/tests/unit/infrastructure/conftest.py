import pytest

from src.backend.app.core.infrastructure.repositories.inmemory import (
    InMemoryAuthAccountRepository,
    InMemoryUserRepository,
)
from src.backend.app.shared.infrastructure.inm_storage import InMemoryStorage


@pytest.fixture
async def inm_storage():
    return InMemoryStorage()


@pytest.fixture
async def user_repo(inm_storage):
    return InMemoryUserRepository(inm_storage)


@pytest.fixture
async def auth_account_repo(inm_storage):
    return InMemoryAuthAccountRepository(inm_storage)
