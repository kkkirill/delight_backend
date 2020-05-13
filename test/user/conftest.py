from random import randint

import pytest
from faker import Faker

from utils.factories import PlaylistFactory, PostFactory


@pytest.fixture
def playlist_qty():
    return 1


@pytest.fixture
def playlists(playlist_qty, user):
    return PlaylistFactory.create_batch(size=playlist_qty, owner=user)


@pytest.fixture
def faker():
    return Faker(locale='en-US')


@pytest.fixture
def post_images(faker):
    return [faker.image_url() for i in range(randint(1, 11))]


@pytest.fixture
def post(post_images, songs, albums, playlists, user):
    return PostFactory.create(
        images=post_images,
        songs=songs,
        albums=albums,
        playlists=playlists,
        owner=user
    )


@pytest.fixture
def post_qty():
    return 1


@pytest.fixture
def posts(post_qty, post_images, songs, albums, playlists, user):
    return PostFactory.create_batch(
        size=post_qty,
        images=post_images,
        songs=songs,
        albums=albums,
        playlists=playlists,
        owner=user
    )
