from rest_framework.fields import SerializerMethodField, ListField
from rest_framework.serializers import ModelSerializer, URLField

from apps.likes import mixin_tools as likes_services
from apps.media.serializers.album import AlbumShortInfoSerializer
from apps.media.serializers.artist import ArtistShortInfoSerializer
from apps.media.serializers.song import SongShortInfoSerializer
from apps.user.models.post import Post
from apps.user.serializers.playlist import PlaylistShortInfoSerializer
from apps.user.serializers.user import UserShortInfoSerializer


class PostSerializer(ModelSerializer):
    songs = SongShortInfoSerializer(many=True, read_only=True)
    albums = AlbumShortInfoSerializer(many=True, read_only=True)
    playlists = PlaylistShortInfoSerializer(many=True, read_only=True)
    images = ListField(child=URLField())
    is_fan = SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'owner', 'pub_date', 'total_likes', 'text', 'images', 'songs', 'playlists', 'albums', 'is_fan')
        read_only_fields = ('pub_date',)

    def get_is_fan(self, obj) -> bool:
        user = self.context.get('request').user
        return likes_services.is_fan(obj, user)


class AlbumsInPostSerializer(AlbumShortInfoSerializer):
    class Meta(AlbumShortInfoSerializer.Meta):
        fields = ('id', 'photo')


class PlaylistInPostSerializer(PlaylistShortInfoSerializer):
    class Meta(PlaylistShortInfoSerializer.Meta):
        fields = ('id', 'photo')


class ArtistInSongInPostSerializer(ArtistShortInfoSerializer):
    class Meta(ArtistShortInfoSerializer.Meta):
        fields = ('id', 'stage_name')


class SongInPostSerializer(SongShortInfoSerializer):
    artists = ArtistInSongInPostSerializer(many=True,)

    class Meta(SongShortInfoSerializer.Meta):
        fields = ('id', 'file', 'artists')


class PostShortInfoSerializer(ModelSerializer):
    owner = UserShortInfoSerializer(read_only=True)
    songs = SongInPostSerializer(many=True, read_only=True)
    albums = AlbumsInPostSerializer(many=True, read_only=True)
    playlists = PlaylistInPostSerializer(many=True, read_only=True)
    images = ListField(child=URLField())

    class Meta(PostSerializer.Meta):
        fields = ('id', 'owner', 'pub_date', 'total_likes', 'text', 'images', 'songs', 'playlists', 'albums')


class PostCUSerializer(ModelSerializer):
    images = ListField(child=URLField())

    class Meta(PostSerializer.Meta):
        fields = ('owner', 'text', 'images', 'songs', 'playlists', 'albums',)

    def get_fields(self, *args, **kwargs):
        fields = super(PostCUSerializer, self).get_fields()
        request = self.context.get('request', None)
        if request and getattr(request, 'method', None) == "PUT":
            for field in fields.values():
                field.required = False
        return fields
