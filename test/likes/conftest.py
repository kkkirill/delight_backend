import pytest


from utils.factories import LikedSongFactory


@pytest.fixture
def liked_song(user, song):
    return LikedSongFactory.create(
        user=user,
        content_object=song
    )


@pytest.fixture
def content_type():
    return 1


@pytest.fixture
def content_obj(content_type, song, album, artist):
    if content_type == 'song':
        return song
    elif content_type == 'artist':
        return artist
    elif content_type == 'album':
        return album
