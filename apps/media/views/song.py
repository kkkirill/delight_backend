from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from apps.media.models.song import Song
from apps.media.serializers.song import (
    SongDetailSerializer, SongShortInfoSerializer)


class SongListView(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('genres', 'artists',)
    http_method_names = ('get',)

    def get_serializer_class(self):
        if getattr(self, 'action', None) == 'list':
            return SongShortInfoSerializer
        return SongDetailSerializer
