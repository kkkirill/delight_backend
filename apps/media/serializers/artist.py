from rest_framework.serializers import ModelSerializer

from apps.media.models.artist import Artist
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
        artist.genres.add(*genres_data)
        return artist

    def update(self, instance, validated_data):
        genres_data = validated_data.pop('genres')
        instance = super(ArtistCUSerializer, self).update(instance,
                                                          validated_data)
        instance.save()
        instance.genres.clear()
        instance.genres.add(*genres_data)
        return instance
