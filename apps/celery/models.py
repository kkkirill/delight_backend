from django.db.models import (
    CASCADE, DateTimeField, FloatField, Model, OneToOneField)

from apps.media.models.song import Song
from apps.user.models import User


class Event(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    song = OneToOneField(Song, on_delete=CASCADE)
    datetime = DateTimeField(auto_now_add=True)
    listen_percentage = FloatField()
