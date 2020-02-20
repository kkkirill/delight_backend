from rest_framework.serializers import ModelSerializer, CharField

from apps.media.models.artist import Artist
from apps.media.models.genre import Genre
from apps.media.serializers.genre import GenreDetailSerializer


class ArtistDetailSerializer(ModelSerializer):
    genres = GenreDetailSerializer(many=True,)

    class Meta:
        model = Artist
        fields = ('url', 'stage_name', 'info', 'photo', 'genres')


class ArtistShortInfoSerializer(ArtistDetailSerializer):
    class Meta(ArtistDetailSerializer.Meta):
        fields = ('url', 'stage_name', 'photo')


class ArtistCUSerializer(ModelSerializer):
    class Meta(ArtistDetailSerializer.Meta):
        pass

    def get_fields(self, *args, **kwargs):
        fields = super(ArtistCUSerializer, self).get_fields(*args, **kwargs)
        request = self.context.get('request', None)
        if request and getattr(request, 'method', None) == "PUT":
            for field in fields.values():
                field.required = False
        return fields

    def create(self, validated_data):
        genres_data = validated_data.pop('genres')
        artist = Artist.objects.create(**validated_data)
        for genre_data in genres_data:
            # artist.genres.add(Genre.objects.get(pk=genre_data))
            artist.genres.add(genre_data)
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
            instance.genres.add(genre_data)
        return instance



