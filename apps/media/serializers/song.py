from rest_framework import serializers
from apps.media.models.song import Song


class SongDetailSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)
    file = serializers.FileField(max_length=None, use_url=True)

    class Meta:
        model = Song
        fields = ('title', 'image', 'file', 'explicit', 'artists', 'genres')
        read_only_fields = ('listens',)

    def create(self, validated_data):
        artists = validated_data.pop('artists')
        genres = validated_data.pop('genres')
        song = Song.objects.create(**validated_data)
        song.artists.add(*artists)
        song.genres.add(*genres)
        return song
