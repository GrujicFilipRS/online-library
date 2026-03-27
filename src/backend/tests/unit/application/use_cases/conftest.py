import pytest

from src.backend.app.core.application.use_cases.auth_account import (
    AutheticateUseCase,
    ChangeAuthProviderIdentifierUseCase,
    LinkAuthProviderUseCase,
    ListAuthProvidersUseCase,
    UnlinkAuthProviderUseCase,
)
from src.backend.app.core.application.use_cases.user import (
    LoginViaPasswordUseCase,
    RegisterViaPasswordUseCase,
)
from src.backend.app.core.application.use_cases.user_auth import LoginViaProviderUseCase
from src.backend.app.core.infrastructure.units_of_work.inmemory import (
    InMemoryAuthAccountUnitOfWork,
    InMemoryUserAuthUnitOfWork,
    InMemoryUserUnitOfWork,
)
from src.backend.app.shared.infrastructure.inm_storage import InMemoryStorage


@pytest.fixture
async def inm_storage():
    return InMemoryStorage()


@pytest.fixture
async def user_uow_factory(inm_storage):
    return lambda: InMemoryUserUnitOfWork(inm_storage)


@pytest.fixture
async def auth_account_uow_factory(inm_storage):
    return lambda: InMemoryAuthAccountUnitOfWork(inm_storage)


@pytest.fixture
async def user_auth_uow_factory(inm_storage):
    return lambda: InMemoryUserAuthUnitOfWork(inm_storage)


@pytest.fixture
async def register_via_password(user_uow_factory):
    return RegisterViaPasswordUseCase(user_uow_factory)


@pytest.fixture
async def login_via_password(user_uow_factory):
    return LoginViaPasswordUseCase(user_uow_factory)


@pytest.fixture
async def authenticate(auth_account_uow_factory):
    return AutheticateUseCase(auth_account_uow_factory)


@pytest.fixture
async def change_auth_provider_identifier(auth_account_uow_factory):
    return ChangeAuthProviderIdentifierUseCase(auth_account_uow_factory)


@pytest.fixture
async def link_auth_provider(auth_account_uow_factory):
    return LinkAuthProviderUseCase(auth_account_uow_factory)


@pytest.fixture
async def list_auth_providers(auth_account_uow_factory):
    return ListAuthProvidersUseCase(auth_account_uow_factory)


@pytest.fixture
async def unlink_auth_provider(auth_account_uow_factory):
    return UnlinkAuthProviderUseCase(auth_account_uow_factory)


@pytest.fixture
async def login_via_auth_provider(user_auth_uow_factory):
    return LoginViaProviderUseCase(user_auth_uow_factory)
