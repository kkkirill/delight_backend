from django.core.exceptions import ValidationError

from vibrer.settings import (ALLOWED_SONG_EXTENSIONS,
                             MAX_UPLOAD_IMAGE_SIZE, MAX_UPLOAD_SONG_SIZE)


def validate_file_size(file):
    size_limit = MAX_UPLOAD_IMAGE_SIZE \
        if hasattr(file, 'image') else MAX_UPLOAD_SONG_SIZE
    file_size = file.size
    if file_size > size_limit * 1024 ** 2:
        raise ValidationError(f'Max size of audio file is {size_limit} MB')
    return file


def validate_audio_file_extension(file):
    extension = file.name.rsplit('.', 1)[-1]
    if extension not in ALLOWED_SONG_EXTENSIONS:
        return ValidationError(f'Audio format not supported. '
                               f'Try using one of {ALLOWED_SONG_EXTENSIONS}')
    return file
