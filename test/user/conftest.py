import pytest

from utils.factories import PlaylistFactory


@pytest.fixture
def playlist_qty():
    return 1


@pytest.fixture
def playlists(playlist_qty, user):
    return PlaylistFactory.create_batch(size=playlist_qty, owner=user)
