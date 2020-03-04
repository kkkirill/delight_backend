import pytest

from apps.media.seed.factories.factories import (
    ArtistFactory, GenreFactory, SongFactory)


@pytest.fixture
def song():
    return SongFactory.create(
        artists=ArtistFactory.create_batch(size=2),
        genres=GenreFactory.create_batch(size=2)
    )


@pytest.fixture
def song_qty():
    return 1


@pytest.fixture
def songs(song_qty):
    return SongFactory.create_batch(size=song_qty)