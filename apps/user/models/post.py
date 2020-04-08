from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import TextField, URLField, DateTimeField, ManyToManyField, Model, ForeignKey, CASCADE

from apps.media.models import Song, Album
from apps.user.models.playlist import Playlist
from . import User


class Post(Model):
    owner = ForeignKey(User, related_name='posts', on_delete=CASCADE)
    text = TextField(blank=True)
    songs = ManyToManyField(Song, related_name='posts', blank=True)
    playlists = ManyToManyField(Playlist, related_name='posts', blank=True)
    albums = ManyToManyField(Album, related_name='posts', blank=True)
    pub_date = DateTimeField(auto_now_add=True)
    likes = GenericRelation('likes.Like', related_query_name='posts')


    @property
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f'{self.pub_date};{self.owner}'


class Image(Model):
    image = URLField()
    post = ForeignKey(Post, related_name='images', on_delete=CASCADE, blank=True, null=True)
