from django.db.models import (BooleanField, CharField, FileField, ImageField,
                              ManyToManyField, Model, PositiveIntegerField)

from utils.utils import generate_upload_path


class Song(Model):
    title = CharField(max_length=200)
    duration = PositiveIntegerField(default=0)
    image = ImageField(default=None, upload_to='media/')
    file = FileField(upload_to=generate_upload_path, default=None)
    listens = PositiveIntegerField(default=0)
    explicit = BooleanField()
    artists = ManyToManyField(artist.Artist, related_name='songs')
    genres = ManyToManyField(genre.Genre, related_name='songs')

    def __str__(self):
        return self.title
