import pytest
from django_redis import get_redis_connection
from rest_auth.app_settings import TokenSerializer, create_token
from rest_auth.models import TokenModel

from utils.factories import (
    AlbumFactory, ArtistFactory, GenreFactory, PlaylistFactory, SongFactory,
    UserFactory)


@pytest.fixture
def redis():
    yield get_redis_connection('default')
    get_redis_connection('default').flushall()


@pytest.fixture
def is_staff():
    return False


@pytest.fixture
def user(is_staff):
    user = UserFactory.create(is_staff=is_staff)
    PlaylistFactory.create(name='Favorites', is_private=True, owner=user)
    PlaylistFactory.create(name='My Songs', is_private=True, owner=user)
    return user


@pytest.fixture
def token(user):
    return create_token(TokenModel, user, TokenSerializer)


@pytest.fixture
def genres():
    return GenreFactory.create_batch(size=2)


@pytest.fixture
def songs_for_added():
    return SongFactory.create_batch(size=4)


@pytest.fixture
def song_qty():
    return 1


@pytest.fixture
def songs(song_qty):
    return SongFactory.create_batch(size=song_qty, explicit=False)


@pytest.fixture
def song():
    return SongFactory.create(
        artists=ArtistFactory.create_batch(size=2),
        genres=GenreFactory.create_batch(size=2)
    )


@pytest.fixture
def artist():
    return ArtistFactory.create(
        genres=GenreFactory.create_batch(size=2)
    )


@pytest.fixture
def album():
    return AlbumFactory.create(
        artists=ArtistFactory.create_batch(size=2),
        genres=GenreFactory.create_batch(size=2),
        songs=SongFactory.create_batch(size=6),
    )


@pytest.fixture
def album_qty():
    return 1


@pytest.fixture
def albums(album_qty):
    return AlbumFactory.create_batch(size=album_qty)


@pytest.fixture
def playlist(user, songs):
    return PlaylistFactory.create(owner=user, is_private=False,
                                  songs=songs)


@pytest.fixture
def artists_for_added():
    return ArtistFactory.create_batch(size=2)
