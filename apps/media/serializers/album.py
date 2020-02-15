from rest_framework.serializers import ModelSerializer
from apps.media.models.album import Album
from apps.media.serializers.artist import ArtistShortInfoSerializer


class AlbumSerializer(ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'
        read_only_fields = ('songs_amount',)


class AlbumDetailSerializer(AlbumSerializer):
    artists = ArtistShortInfoSerializer(many=True,)
