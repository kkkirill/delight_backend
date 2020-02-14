# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.auth.models import User as BaseUser
# from django.db.models import (Model, CharField, PositiveIntegerField, ImageField,
#                               BooleanField, ManyToManyField, ForeignKey, CASCADE)
#
#
# class User(BaseUser):
#     photo = ImageField(upload_to='', default='')
#     playlists = ManyToManyField('Playlist', related_name='users')
#     followers = ManyToManyField('User', related_name='followings')
#
#
# class Playlist(Model):
#     name = CharField(max_length=200, unique=True)
#     is_private = BooleanField()
#     songs = ManyToManyField('Song', related_name='playlists')
#
#
# class Liked(Model):
#     ARTIST = 'AR'
#     SONG = 'SG'
#     PLAYLIST = 'PT'
#     ALBUM = 'AM'
#     LIKED_CHOICES = (
#         (ARTIST, 'Artist'),
#         (SONG, 'Song'),
#         (PLAYLIST, 'Playlist'),
#         (ALBUM, 'Album'),
#     )
#     content_type = CharField(choices=LIKED_CHOICES)
#     object_id = PositiveIntegerField()
#     content_object = GenericForeignKey(content_type, object_id)
#     user = ForeignKey(User, related_name='relations', on_delete=CASCADE)
