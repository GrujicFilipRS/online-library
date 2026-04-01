import pytest
from uuid import uuid4

from src.backend.app.core.domain.exceptions import (
    AuthorAlreadyExistsError,
    AuthorNotFoundError,
)

from src.backend.app.core.infrastructure.services import AuthorService


@pytest.fixture
async def author_service(author_repo):
    return AuthorService(author_repo)


async def test_create_and_get_author_successfully(author_service: AuthorService):
    name = "Osip Mandelstam"
    nationality = "Russian"
    image_url = "https://upload.wikimedia.org/wikipedia/commons/4/40/Mandelshtam17.jpg"

    author = await author_service.create_author(name=name, nationality=nationality, image_url=image_url)
    get_author = await author_service.get_author_details(author.author_id)

    assert get_author.name.value == author.name.value
    assert get_author.image_url.value == author.image_url.value
    assert get_author.nationality == author.nationality

async def test_create_author_null_image(author_service: AuthorService):
    name = "Osip Mandelstam"
    nationality = "Russian"
    image_url = None

    author = await author_service.create_author(name=name, nationality=nationality, image_url=image_url)
    get_author = await author_service.get_author_details(author.author_id)

    assert get_author.name.value == author.name.value
    assert get_author.image_url.value == author.image_url.value
    assert get_author.nationality == author.nationality

async def test_create_existing_author_raises(author_service: AuthorService):
    name = "Osip Mandelstam"
    nationality = "Russian"
    image_url = "https://upload.wikimedia.org/wikipedia/commons/4/40/Mandelshtam17.jpg"

    await author_service.create_author(name=name, nationality=nationality, image_url=image_url)

    with pytest.raises(AuthorAlreadyExistsError):
        await author_service.create_author(name=name, nationality=nationality, image_url=image_url)


async def test_get_undefined_author_raises(author_service: AuthorService):
    with pytest.raises(AuthorNotFoundError):
        await author_service.get_author_details(uuid4())

async def test_get_deleted_user_raises(author_service: AuthorService):
    name = "Osip Mandelstam"
    nationality = "Russian"
    image_url = "https://upload.wikimedia.org/wikipedia/commons/4/40/Mandelshtam17.jpg"

    author = await author_service.create_author(name=name, nationality=nationality, image_url=image_url)
    await author_service.delete_author(author.author_id)
    with pytest.raises(AuthorNotFoundError):
        get_author = await author_service.get_author_details(author.author_id)

async def test_list_authors(author_service: AuthorService):
    name = "Osip Mandelstam"
    nationality = "Russian"
    image_url = "https://upload.wikimedia.org/wikipedia/commons/4/40/Mandelshtam17.jpg"

    authors = await author_service.list_authors(offset=0, limit=1)
    assert not authors
    author = await author_service.create_author(name=name, nationality=nationality, image_url=image_url)

    authors = await author_service.list_authors(offset=0, limit=1)
    assert author.author_id == authors[0].author_id
    assert author.name == authors[0].name
    assert author.image_url== authors[0].image_url
    assert author.nationality== authors[0].nationality

async def test_search_by_name(author_service: AuthorService):
    name = "Osip Mandelstam"
    nationality = "Russian"
    image_url = "https://upload.wikimedia.org/wikipedia/commons/4/40/Mandelshtam17.jpg"

    authors = await author_service.search_by_name(name="Osip",offset=0, limit=1)
    assert not authors
    author = await author_service.create_author(name=name, nationality=nationality, image_url=image_url)

    authors = await author_service.search_by_name(name="Osip", offset=0, limit=1)

    assert author.author_id == authors[0].author_id
    assert author.name == authors[0].name
    assert author.image_url== authors[0].image_url
    assert author.nationality== authors[0].nationality

async def test_update_undefined_raises(author_service: AuthorService):
    name = "Osip Mandelstam"
    nationality = "Russian"
    image_url = "https://upload.wikimedia.org/wikipedia/commons/4/40/Mandelshtam17.jpg"

    with pytest.raises(AuthorNotFoundError):
        await author_service.update_author(author_id=uuid4(), name=name, nationality=nationality, image_url=image_url)

async def test_update(author_service: AuthorService):
    name = "Osip Mandelstam"
    nationality = "Russian"
    image_url = "https://upload.wikimedia.org/wikipedia/commons/4/40/Mandelshtam17.jpg"

    new_name = "Vladimir Mayakovsky"
    new_nationality = "Soviet"
    new_image_url = "https://upload.wikimedia.org/wikipedia/commons/3/33/Mayakovsky-1910.jpg"

    author = await author_service.create_author(name=name, nationality=nationality, image_url=image_url)
    updated_author = await author_service.update_author(author_id=author.author_id, name=new_name, nationality=new_nationality, image_url=new_image_url)
    get_author = await author_service.get_author_details(author.author_id)

    assert updated_author.name.value == get_author.name.value == new_name
    assert updated_author.nationality == get_author.nationality == new_nationality
    assert updated_author.image_url.value == get_author.image_url.value == new_image_url

