import pytest

from utils.factories import AlbumFactory, ArtistFactory


@pytest.fixture
def artist_qty():
    return 1


@pytest.fixture
def artists(artist_qty):
    return ArtistFactory.create_batch(size=artist_qty)

