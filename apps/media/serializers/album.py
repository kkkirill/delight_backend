from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from apps.likes import mixin_tools as likes_services
from apps.media.models.album import Album
from apps.media.serializers.artist import ArtistShortInfoSerializer
from apps.media.serializers.genre import GenreDetailSerializer
from apps.media.serializers.song import SongShortInfoSerializer


class AlbumDetailSerializer(ModelSerializer):
    genres = GenreDetailSerializer(many=True,)
    songs = SongShortInfoSerializer(many=True,)
    artists = ArtistShortInfoSerializer(many=True, )
    is_fan = SerializerMethodField()

    class Meta:
        model = Album
        fields = ('url', 'title', 'songs_amount', 'photo',
                  'release_year', 'artists', 'genres', 'songs', 'total_likes',
                  'is_fan')
        read_only_fields = ('songs_amount',)

    def get_is_fan(self, obj) -> bool:
        user = self.context.get('request').user
        return likes_services.is_fan(obj, user)


class AlbumShortInfoSerializer(AlbumDetailSerializer):
    class Meta(AlbumDetailSerializer.Meta):
        fields = ('url', 'title', 'photo', 'artists')


class AlbumCUSerializer(ModelSerializer):
    class Meta(AlbumDetailSerializer.Meta):
        fields = ('url', 'title', 'songs_amount', 'photo',
                  'release_year', 'artists', 'genres', 'songs')

    def get_fields(self, *args, **kwargs):
        fields = super(AlbumCUSerializer, self).get_fields()
        request = self.context.get('request', None)
        if request and getattr(request, 'method', None) == "PUT":
            for field in fields.values():
                field.required = False
        return fields

    def create(self, validated_data):
        genres_data = validated_data.pop('genres')
        artists_data = validated_data.pop('artists')
        songs_data = validated_data.pop('songs')
        album = Album.objects.create(**validated_data)
        album.genres.set(genres_data)
        album.artists.set(artists_data)
        album.songs.set(songs_data)
        return album

    def update(self, instance, validated_data):
        genres_data = validated_data.pop('genres', None)
        artists_data = validated_data.pop('artists', None)
        songs_data = validated_data.pop('songs', None)
        instance = super(AlbumCUSerializer, self).update(instance,
                                                         validated_data)
        instance.save()
        if genres_data:
            instance.genres.set(genres_data)
        if artists_data:
            instance.artists.set(artists_data)
        if songs_data:
            instance.songs.set(songs_data)
        return instance
