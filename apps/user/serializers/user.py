from django.contrib.auth import authenticate, get_user_model
from rest_framework.serializers import (
    CharField, HyperlinkedRelatedField, ModelSerializer,
    Serializer, ValidationError)

from apps.likes.serializers.like import LikeSerializer
from delight.settings import FAVORITES_PLAYLIST_NAME, MY_SONGS_PLAYLIST_NAME

User = get_user_model()


class UserRegistrationSerializer(ModelSerializer):
    password = CharField(max_length=128, write_only=True)
    token = CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'token')

    def create(self, validated_data):
        user: User = User.objects.create_user(**validated_data)
        user.playlists.create(name=FAVORITES_PLAYLIST_NAME, is_private=True)
        user.playlists.create(name=MY_SONGS_PLAYLIST_NAME, is_private=True)
        user.save()
        return user


class UserLoginSerializer(Serializer):
    username = CharField(max_length=50)
    password = CharField(max_length=128, style={'input_type': 'password'},
                         write_only=True)
    token = CharField(max_length=100, read_only=True)

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if username and password:
            user = authenticate(username=username, password=password)

            if user is None:
                raise ValidationError(
                    'Provided credentials don\'t match any existing user')

        else:
            raise ValidationError(
                'Both username and password are required for authentication')

        data['user'] = user
        return data


class UserSerializer(ModelSerializer):
    followers = HyperlinkedRelatedField(many=True, read_only=True, view_name='user-detail')
    following = HyperlinkedRelatedField(many=True, read_only=True, view_name='user-detail')
    password = CharField(max_length=128, write_only=True,
                         style={'input_type': 'password'})
    likes = LikeSerializer(many=True, )

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'photo', 'followers',
                  'followers_amount', 'is_staff', 'likes', 'following')


class UserShortInfoSerializer(ModelSerializer):
    class Meta(UserSerializer.Meta):
        fields = ('id', 'username', 'photo', 'followers', 'followers_amount')
