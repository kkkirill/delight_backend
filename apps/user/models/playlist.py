from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import (
    CASCADE, BooleanField, CharField, ForeignKey, ManyToManyField, Model, UniqueConstraint, URLField)

from apps.media.models.song import Song
from apps.user.models.user import User
from delight.settings import STATIC_CLOUDFRONT_DOMAIN, DEFAULT_MEDIA_LOGO_FILENAME
from delight.validators import CustomURLValidator


class Playlist(Model):
    name = CharField(max_length=200)
    photo = URLField(default=f'{STATIC_CLOUDFRONT_DOMAIN}/default/{DEFAULT_MEDIA_LOGO_FILENAME}',
                     validators=[CustomURLValidator])
    songs = ManyToManyField(Song, related_name='playlists')
    is_private = BooleanField(default=False)
    owner = ForeignKey(User, related_name='playlists', on_delete=CASCADE)
    likes = GenericRelation('likes.Like', related_query_name='playlists')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['owner', 'name'], name='unique_playlist_name_per_user_constraint')
        ]

    @property
    def songs_amount(self):
        return self.songs.count()

    @property
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.name
