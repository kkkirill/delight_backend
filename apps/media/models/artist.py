from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import (
    CharField, ManyToManyField, Model, TextField, URLField)

from apps.likes.models.like import Like


class Artist(Model):
    stage_name = CharField(max_length=200)
    info = TextField(blank=True)
    photo = URLField(default='image.png')
    genres = ManyToManyField('Genre', related_name='artists')
    likes = GenericRelation(Like, related_query_name='artists')

    def __str__(self):
        return self.stage_name

    @property
    def total_likes(self):
        return self.likes.count()
