from rest_framework.serializers import ModelSerializer

from apps.media.models.artist import Artist
from apps.media.serializers.genre import GenreDetailSerializer


class ArtistSerializer(ModelSerializer):
    genres = GenreDetailSerializer(many=True,)

    class Meta:
        model = Artist
        fields = ('url', 'stage_name', 'info', 'photo', 'genres')


class ArtistShortInfoSerializer(ArtistSerializer):
    class Meta(ArtistSerializer.Meta):
        fields = ('url', 'stage_name')
