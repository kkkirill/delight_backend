from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from apps.media.models.song import Song
from apps.media.serializers.song import (
    SongCUSerializer, SongDetailSerializer, SongShortInfoSerializer)


class SongView(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('genres', 'artists',)
    http_method_names = ('get', 'post', 'put')

    def get_serializer_class(self):
        method = getattr(self.request, 'method', None)
        action = getattr(self, 'action', None)
        if self.request and method == 'GET':
            if action == 'list':
                return SongShortInfoSerializer
            elif action == 'retrieve':
                return SongDetailSerializer
        elif self.request and method in ('POST', 'PUT'):
            return SongCUSerializer
