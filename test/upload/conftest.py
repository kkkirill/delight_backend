from typing import Any

import pytest
from rest_auth.models import TokenModel
from rest_auth.app_settings import TokenSerializer, create_token

from utils.factories import (
    ArtistFactory, GenreFactory, SongFactory, UserFactory)
from utils.upload_file import FileUploaderS3


@pytest.fixture
def is_staff():
    return False


@pytest.fixture
def user(is_staff):
    return UserFactory.create(is_staff=is_staff)


@pytest.fixture
def token(user):
    return create_token(TokenModel, user, TokenSerializer)


@pytest.fixture
def song():
    return SongFactory.create(
        artists=ArtistFactory.create_batch(size=2),
        genres=GenreFactory.create_batch(size=2)
    )

@pytest.fixture
def artists():
    return ArtistFactory.create_batch(size=2)


@pytest.fixture
def genres():
    return GenreFactory.create_batch(size=2)


@pytest.fixture
def keys():
    file_uploader = FileUploaderS3()
    ikey = file_uploader.upload_file_to_s3('media/dingo.png')
    fkey = file_uploader.upload_file_to_s3('media/song.mp3')
    yield {'ikey': ikey, 'fkey': fkey}
    file_uploader.delete_file(ikey)
    file_uploader.delete_file(fkey)
    open('.localstack/data/s3_api_calls.json', 'w').close()
