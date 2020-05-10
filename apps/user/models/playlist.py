from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import (
    CASCADE, BooleanField, CharField, ForeignKey, ManyToManyField, Model)

from apps.media.models.song import Song
from apps.user.models.user import User


class Playlist(Model):
    name = CharField(max_length=200)
    songs = ManyToManyField(Song, related_name='playlists')
    is_private = BooleanField(default=False)
    owner = ForeignKey(User, related_name='playlists', on_delete=CASCADE)
    likes = GenericRelation('likes.Like', related_query_name='playlists')

    @property
    def songs_amount(self):
        return self.songs.count()

    @property
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.name
