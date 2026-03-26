import pytest

from src.backend.app.core.infrastructure.repositories.inmemory import (
    InMemoryUserRepository,
)
from src.backend.app.shared.infra.inm_storage import InMemoryStorage


@pytest.fixture
async def inm_storage():
    return InMemoryStorage()


@pytest.fixture
async def user_repo(inm_storage):
    return InMemoryUserRepository(inm_storage)
