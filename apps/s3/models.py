from django.db.models import Model, FileField, CharField

from apps.s3.storages import StaticStorage
from apps.s3.utils import get_filepath, check_file_size


class File(Model):
    ALBUM_IMAGE = 'ALI'
    ARTIST_IMAGE = 'ARI'
    SONG_IMAGE = 'SI'
    SONG_FILE = 'SF'
    POST_IMAGE = 'PI'
    USER_IMAGE = 'UI'
    FILE_TYPES = (
        (ALBUM_IMAGE, 'album_image'),
        (ARTIST_IMAGE, 'artist_image'),
        (SONG_IMAGE, 'song_image'),
        (SONG_FILE, 'song_file'),
        (POST_IMAGE, 'post_image'),
        (USER_IMAGE, 'user_image'),
    )
    FILE_TYPES_PATHS = {
        ALBUM_IMAGE: '/album/',
        ARTIST_IMAGE: '/artist/',
        SONG_IMAGE: '/song/img/',
        SONG_FILE: '/song/file/',
        POST_IMAGE: '/post/',
        USER_IMAGE: '/user/'
    }
    file = FileField(upload_to=get_filepath, validators=[check_file_size], storage=StaticStorage())
    type = CharField(choices=FILE_TYPES, max_length=12)
