from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import TextField, SET_NULL, URLField, DateTimeField, ManyToManyField, Model

from apps.likes.models import Like, CASCADE, ForeignKey, User
from apps.media.models import Song, Album
from apps.user.models.playlist import Playlist


class Post(Model):
    owner = ForeignKey(User, related_name='posts', on_delete=CASCADE)
    text = TextField(blank=True)
    songs = ManyToManyField(Song, related_name='posts', on_delete=SET_NULL, blank=True)
    playlists = ManyToManyField(Playlist, related_name='posts', on_delete=SET_NULL, blank=True)
    albums = ForeignKey(Album, related_name='posts', on_delete=SET_NULL, blank=True)
    pub_date = DateTimeField()
    likes = GenericRelation(Like, related_query_name='posts')

    @property
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f'{self.pub_date};{self.owner}'


class Image:
    image = URLField()
    post = ForeignKey(Post, related_name='images', on_delete=CASCADE)
