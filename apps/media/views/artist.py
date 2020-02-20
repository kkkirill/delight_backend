from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from apps.media.models.artist import Artist
from apps.media.serializers.artist import (
    ArtistCUSerializer, ArtistDetailSerializer, ArtistShortInfoSerializer)


class ArtistListView(viewsets.ModelViewSet):
    serializer_class = ArtistDetailSerializer
    queryset = Artist.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('genres',)
    http_method_names = ('get', 'post', 'put')

    def get_serializer_class(self):
        if self.request and getattr(self.request, 'method', None) == "GET":
            if getattr(self, 'action', None) == 'list':
                return ArtistShortInfoSerializer
            elif getattr(self, 'action', None) == 'retrieve':
                return ArtistDetailSerializer
        elif self.request and getattr(self.request, 'method', None) == "POST" \
                or self.request and getattr(self.request, 'method', None) == "PUT":
            return ArtistCUSerializer
