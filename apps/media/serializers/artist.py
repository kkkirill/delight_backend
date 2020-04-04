from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from apps.likes import mixin_tools as likes_services
from apps.media.models.artist import Artist
from apps.media.serializers.genre import GenreDetailSerializer


class ArtistDetailSerializer(ModelSerializer):
    genres = GenreDetailSerializer(many=True,)
    is_fan = SerializerMethodField()

    class Meta:
        model = Artist
        fields = ('url', 'stage_name', 'info', 'photo', 'genres', 'is_fan')

    def get_is_fan(self, obj) -> bool:
        user = self.context.get('request').user
        return likes_services.is_fan(obj, user)


class ArtistShortInfoSerializer(ArtistDetailSerializer):
    class Meta(ArtistDetailSerializer.Meta):
        fields = ('url', 'stage_name', 'photo')


class ArtistCUSerializer(ModelSerializer):
    class Meta(ArtistDetailSerializer.Meta):
        fields = ('url', 'stage_name', 'info', 'photo', 'genres')

    def get_fields(self, *args, **kwargs):
        fields = super(ArtistCUSerializer, self).get_fields()
        request = self.context.get('request', None)
        if request and getattr(request, 'method', None) == "PUT":
            for field in fields.values():
                field.required = False
        return fields

    def create(self, validated_data):
        genres_data = validated_data.pop('genres')
        artist = Artist.objects.create(**validated_data)
        artist.genres.set(genres_data)
        return artist

    def update(self, instance, validated_data):
        genres_data = validated_data.pop('genres', None)
        instance = super(ArtistCUSerializer, self).update(instance,
                                                          validated_data)
        instance.save()
        if genres_data:
            instance.genres.set(genres_data)
        return instance
