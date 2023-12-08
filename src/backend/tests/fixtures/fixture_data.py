import tempfile

import pytest

from posts.models import Post


@pytest.fixture()
def mock_media(settings):
    with tempfile.TemporaryDirectory() as temp_directory:
        settings.MEDIA_ROOT = temp_directory
        yield temp_directory


@pytest.fixture
def post_1(user):
    image = tempfile.NamedTemporaryFile(suffix=".jpg").name
    post = Post.objects.create(
        name='TestPost',
        text='TextTestPost',
        author=user,
        image=image
    )
    return post


@pytest.fixture
def post_2(user):
    image = tempfile.NamedTemporaryFile(suffix=".jpg").name
    post = Post.objects.create(
        name='TestPost2',
        text='TextTestPost2',
        author=user,
        image=image
    )
    return post
