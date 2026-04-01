from uuid import UUID

from src.backend.app.core.domain.models import Author
from src.backend.app.core.domain.value_objects import AuthorName, ImageURL


async def test_author_create_success():
    name = "George Orwell"
    nationality = "Englih"
    image_url = "https://upload.wikimedia.org/wikipedia/commons/7/7e/George_Orwell_press_photo.jpg"

    author = Author.create(name=name, nationality=nationality, image_url=image_url)

    assert isinstance(author.author_id, UUID)
    assert isinstance(author.name, AuthorName)
    assert isinstance(author.image_url, ImageURL)
    assert author.name.value == name
    assert author.image_url.value == image_url

async def test_author_create_success_no_image():
    name = "George Orwell"
    nationality = "Englih"
    image_url = None

    author = Author.create(name=name, nationality=nationality, image_url=image_url)

    assert isinstance(author.author_id, UUID)
    assert isinstance(author.name, AuthorName)
    assert author.name.value == name
