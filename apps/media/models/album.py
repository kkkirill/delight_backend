from django.db.models import (
    CharField, DateField, ManyToManyField, Model,
    PositiveSmallIntegerField, URLField)


class Album(Model):
    title = CharField(max_length=200)
    songs_amount = PositiveSmallIntegerField(default=0)
    photo = URLField(default='image.png')
    release_year = DateField()
    artists = ManyToManyField('Artist', related_name='albums')
    genres = ManyToManyField('Genre', related_name='albums')
    songs = ManyToManyField('Song', related_name='albums')

    def __str__(self):
        return self.title
