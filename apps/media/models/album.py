from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import (
    CharField, DateField, ManyToManyField, Model, PositiveSmallIntegerField,
    URLField)

from apps.likes.models.like import Like
from delight.settings import DEFAULT_MEDIA_LOGO_FILENAME, STATIC_CLOUDFRONT_DOMAIN
from delight.validators import CustomURLValidator


class Album(Model):
    title = CharField(max_length=200)
    songs_amount = PositiveSmallIntegerField(default=0)
    photo = URLField(default=f'{STATIC_CLOUDFRONT_DOMAIN}/default/{DEFAULT_MEDIA_LOGO_FILENAME}',
                     validators=[CustomURLValidator])
    release_year = DateField()
    artists = ManyToManyField('Artist', related_name='albums')
    genres = ManyToManyField('Genre', related_name='albums')
    songs = ManyToManyField('Song', related_name='albums')
    likes = GenericRelation(Like, related_query_name='albums')

    def __str__(self):
        return self.title

    @property
    def total_likes(self):
        return self.likes.count()
