from django.contrib.contenttypes.models import ContentType

from apps.likes.models import Like
from apps.media.models import Song
from apps.user.models.user import User
from delight.settings import FAVORITES_PLAYLIST_NAME


def add_like(obj, user):
    obj_type = ContentType.objects.get_for_model(obj)
    like, is_created = Like.objects.get_or_create(
        content_type=obj_type, object_id=obj.id, user=user)

    if (not user.is_anonymous) and isinstance(obj, Song):
        favorites = user.playlists.get(name=FAVORITES_PLAYLIST_NAME)
        favorites.songs.add(like.content_object)
    return like


def remove_like(obj, user):
    obj_type = ContentType.objects.get_for_model(obj)
    Like.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user
    ).delete()

    if (not user.is_anonymous) and isinstance(obj, Song):
        favorites = user.playlists.get(name=FAVORITES_PLAYLIST_NAME)
        favorites.songs.remove(obj)


def is_fan(obj, user) -> bool:
    if not user.is_authenticated:
        return False
    obj_type = ContentType.objects.get_for_model(obj)
    likes = Like.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user)
    return likes.exists()


def get_fans(obj):
    obj_type = ContentType.objects.get_for_model(obj)
    return User.objects.filter(
        likes__content_type=obj_type, likes__object_id=obj.id)


def add_follower(obj, user):
    obj.followers.add(user)
    obj.followers_amount += 1
    obj.save()


def remove_follower(obj, user):
    obj.followers.remove(user)
    obj.followers_amount -= 1
    obj.save()
