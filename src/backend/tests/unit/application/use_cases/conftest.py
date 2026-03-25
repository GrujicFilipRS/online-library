import pytest

from src.backend.app.core.application.use_cases.user import (
    LoginViaPasswordUseCase,
    RegisterViaPasswordUseCase,
)
from src.backend.app.core.infrastructure.units_of_work.inmemory import (
    InMemoryUserUnitOfWork,
)
from src.backend.app.shared.infra.inm_storage import InMemoryStorage


@pytest.fixture
async def inm_storage():
    return InMemoryStorage()


@pytest.fixture
async def user_uow_factory(inm_storage):
    return lambda: InMemoryUserUnitOfWork(inm_storage)


@pytest.fixture
async def register_via_password(user_uow_factory):
    return RegisterViaPasswordUseCase(user_uow_factory)


@pytest.fixture
async def login_via_password(user_uow_factory):
    return LoginViaPasswordUseCase(user_uow_factory)
