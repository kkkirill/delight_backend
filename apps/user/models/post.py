from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import ArrayField
from django.db.models import TextField, URLField, DateTimeField, ManyToManyField, Model, ForeignKey, CASCADE

from apps.media.models import Song, Album
from apps.user.models.playlist import Playlist
from . import User


class Post(Model):
    owner = ForeignKey(User, related_name='posts', null=True, on_delete=CASCADE)
    text = TextField(blank=True)
    songs = ManyToManyField(Song, related_name='posts', blank=True)
    playlists = ManyToManyField(Playlist, related_name='posts', blank=True)
    albums = ManyToManyField(Album, related_name='posts', blank=True)
    pub_date = DateTimeField(auto_now_add=True)
    images = ArrayField(URLField(), size=10, blank=True, default=list)
    likes = GenericRelation('likes.Like', related_query_name='posts', on_delete=CASCADE)

    @property
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f'{self.pub_date};{self.owner}'
