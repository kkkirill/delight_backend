from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import (
    CharField, ManyToManyField, Model, TextField, URLField)

from delight.settings import DEFAULT_USER_LOGO_FILENAME, STATIC_CLOUDFRONT_DOMAIN
from delight.validators import CustomURLValidator


class Artist(Model):
    stage_name = CharField(max_length=200)
    info = TextField(blank=True)
    photo = URLField(default=f'{STATIC_CLOUDFRONT_DOMAIN}/default/{DEFAULT_USER_LOGO_FILENAME}',
                     validators=[CustomURLValidator])
    genres = ManyToManyField('Genre', related_name='artists')
    likes = GenericRelation('likes.Like', related_query_name='artists')

    def __str__(self):
        return self.stage_name

    @property
    def total_likes(self):
        return self.likes.count()
