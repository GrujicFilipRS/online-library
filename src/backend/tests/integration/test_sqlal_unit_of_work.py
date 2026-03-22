import pytest

from src.backend.app.core.domain.models import User
from src.backend.app.core.infrastructure.repositories.sqlal import (
    SqlAlchemyUserRepository,
)
from src.backend.app.core.infrastructure.units_of_work.sqlal import (
    SqlAlchemyUserUnitOfWork,
)


@pytest.fixture
async def user_uow_factory(db_sess):
    return lambda: SqlAlchemyUserUnitOfWork(db_sess)


@pytest.fixture
async def user_repo_factory(db_sess):
    return lambda: SqlAlchemyUserRepository(db_sess)


async def test_uow_commit_persists_data(
    user_uow_factory,
    user_repo_factory,
):
    async with user_uow_factory() as user_uow:
        user1 = User.create("ril7373", "73")
        user2 = User.create("ril3737", "37")
        await user_uow.user_repo.save(user1)
        await user_uow.user_repo.save(user2)

    user_repo = user_repo_factory()
    get_user1 = await user_repo.get_by_id(user1.user_id)
    assert isinstance(get_user1, User)

    get_user2 = await user_repo.get_by_id(user2.user_id)
    assert isinstance(get_user2, User)


async def test_uow_rollback_on_exception(
    user_uow_factory,
    user_repo_factory,
):
    class TestError(BaseException):
        pass

    with pytest.raises(TestError):
        async with user_uow_factory() as user_uow:
            user1 = User.create("ril7373", "73")
            user2 = User.create("ril3737", "37")
            await user_uow.user_repo.save(user1)
            await user_uow.user_repo.save(user2)
            raise TestError()

    user_repo = user_repo_factory()
    get_user1 = await user_repo.get_by_id(user1.user_id)
    assert get_user1 is None

    user_repo = user_repo_factory()
    get_user2 = await user_repo.get_by_id(user2.user_id)
    assert get_user2 is None
