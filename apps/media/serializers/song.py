from rest_framework import serializers
from apps.media.models.song import Song


class SongDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'
        read_only_fields = ('listens', 'duration')
