import pytest

from apps.media.seed.factories.factories import ArtistFactory, GenreFactory


@pytest.fixture
def artist():
    return ArtistFactory.create(
        genres=GenreFactory.create_batch(size=2)
    )


@pytest.fixture
def artist_qty():
    return 1


@pytest.fixture
def artists(artist_qty):
    return ArtistFactory.create_batch(size=artist_qty)
