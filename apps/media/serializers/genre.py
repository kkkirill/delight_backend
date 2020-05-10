from rest_framework.serializers import ModelSerializer

from apps.media.models.genre import Genre


class GenreDetailSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')
        extra_kwargs = {
            'name': {'validators': []},
        }
