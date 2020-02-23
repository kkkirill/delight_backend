import pytest
from apps.media.seed.factories.factories import SongFactory
from pytest_factoryboy import register

register(SongFactory, 'song')


@pytest.fixture
def song_qty():
    return 1


@pytest.fixture
def songs(song_qty):
    return SongFactory.create_batch(size=song_qty)