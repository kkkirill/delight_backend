from rest_framework import serializers
from apps.media.models.genre import Genre


class GenreDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
