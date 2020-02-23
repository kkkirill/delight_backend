from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from apps.media.models.artist import Artist
from apps.media.serializers.artist import (
    ArtistCUSerializer, ArtistDetailSerializer, ArtistShortInfoSerializer)


class ArtistView(viewsets.ModelViewSet):
    serializer_class = ArtistDetailSerializer
    queryset = Artist.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('genres',)
    http_method_names = ('get', 'post', 'put')

    def get_serializer_class(self):
        method = getattr(self.request, 'method', None)
        action = getattr(self, 'action', None)
        if self.request and method == "GET":
            if action == 'list':
                return ArtistShortInfoSerializer
            elif action == 'retrieve':
                return ArtistDetailSerializer
        elif self.request and method in ('POST', 'PUT'):
            return ArtistCUSerializer
