from rest_framework import serializers

from apps.likes.models.like import Like
from apps.user.models.user import User


class FanSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('object_id', 'content_type', 'like_type')
