from rest_framework.serializers import ModelSerializer

from apps.media.models.artist import Artist
from apps.media.models.genre import Genre
from apps.media.serializers.genre import GenreDetailSerializer


class ArtistSerializer(ModelSerializer):
    genres = GenreDetailSerializer(many=True,)

    class Meta:
        model = Artist
        fields = ('url', 'stage_name', 'info', 'photo', 'genres')

    def create(self, validated_data):
        genres_data = validated_data.pop('genres')
        artist = Artist.objects.create(**validated_data)
        for genre_data in genres_data:
            artist.genres.add(Genre.objects.get(**genre_data))
        return artist

    def update(self, instance, validated_data):
        genres_data = validated_data.pop('genres')
        instance.stage_name = validated_data.get('stage_name',
                                                 instance.stage_name)
        instance.info = validated_data.get('info', instance.info)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.save()
        instance.genres.clear()
        for genre_data in genres_data:
            instance.genres.add(Genre.objects.get(**genre_data))
        return instance


class ArtistShortInfoSerializer(ArtistSerializer):
    class Meta(ArtistSerializer.Meta):
        fields = ('url', 'stage_name')
