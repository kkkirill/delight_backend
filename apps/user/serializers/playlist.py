from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueTogetherValidator

from apps.likes import mixin_tools as likes_services
from apps.media.serializers.song import SongShortInfoSerializer
from apps.user.models.playlist import Playlist
from apps.user.serializers.user import UserShortInfoSerializer


class PlaylistSerializer(ModelSerializer):
    owner = UserShortInfoSerializer(read_only=True)
    songs = SongShortInfoSerializer(many=True, )
    is_fan = SerializerMethodField()

    class Meta:
        model = Playlist
        fields = ('id', 'name', 'photo', 'songs', 'songs_amount', 'is_private', 'owner',
                  'is_fan', 'total_likes')
        read_only_fields = ('songs_amount',)

    def get_is_fan(self, obj) -> bool:
        user = self.context.get('request').user
        return likes_services.is_fan(obj, user)


class PlaylistShortInfoSerializer(ModelSerializer):
    class Meta(PlaylistSerializer.Meta):
        fields = ('id', 'name', 'photo', 'owner')


class PlaylistCUSerializer(ModelSerializer):
    class Meta(PlaylistSerializer.Meta):
        fields = ('id', 'name', 'is_private', 'photo', 'owner')
        validators = [
            UniqueTogetherValidator(
                queryset=Playlist.objects.all(),
                fields=('owner', 'name')
            )
        ]

    def get_fields(self, *args, **kwargs):
        fields = super(PlaylistCUSerializer, self).get_fields()
        request = self.context.get('request', None)
        if request and getattr(request, 'method', None) == "PUT":
            for field in fields.values():
                field.required = False
        return fields


class SongsInPlaylistSerializer(ModelSerializer):
    class Meta(PlaylistSerializer.Meta):
        fields = ('songs',)

    def create(self, validated_data):
        songs_data = validated_data.pop('songs', None)
        playlist_id = self._context['view'].kwargs['parent_lookup_playlist']
        playlist = Playlist.objects.get(id=playlist_id)
        playlist.songs.add(*songs_data)
        return playlist
