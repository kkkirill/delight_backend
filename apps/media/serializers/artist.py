from rest_framework import serializers
from apps.media.models.artist import Artist


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'


class ArtistShortInfoSerializer(ArtistSerializer):
    class Meta(ArtistSerializer.Meta):
        fields = ('stage_name', 'photo',)
