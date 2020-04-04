from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import (
    CASCADE, CharField, ForeignKey, Model, PositiveIntegerField)

from apps.user.models.user import User


class Like(Model):
    user = ForeignKey(User, related_name='likes', on_delete=CASCADE)
    content_type = ForeignKey(ContentType, on_delete=CASCADE)
    object_id = PositiveIntegerField()
    content_object = GenericForeignKey()
