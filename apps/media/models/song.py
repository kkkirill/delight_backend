from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import (
    BooleanField, CharField, ManyToManyField, Model, PositiveIntegerField,
    URLField)

from apps.likes.models.like import Like
from delight.settings import DEFAULT_MEDIA_LOGO_FILENAME, STATIC_CLOUDFRONT_DOMAIN
from delight.validators import CustomURLValidator


class Song(Model):
    title = CharField(max_length=200)
    duration = PositiveIntegerField(default=0)
    image = URLField(default=f'{STATIC_CLOUDFRONT_DOMAIN}/default/{DEFAULT_MEDIA_LOGO_FILENAME}',
                     validators=[CustomURLValidator])
    file = URLField(blank=False, validators=[CustomURLValidator])
    listens = PositiveIntegerField(default=0)
    explicit = BooleanField(default=False)
    artists = ManyToManyField('Artist', related_name='songs')
    genres = ManyToManyField('Genre', related_name='songs')
    likes = GenericRelation(Like, related_query_name='songs')

    def __str__(self):
        return self.title

    @property
    def total_likes(self):
        return self.likes.count()
