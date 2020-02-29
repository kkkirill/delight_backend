from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from apps.media.models.artist import Artist
from apps.media.serializers.artist import (
    ArtistSerializer, ArtistShortInfoSerializer)


class ArtistListView(viewsets.ModelViewSet):
    serializer_class = ArtistSerializer
    queryset = Artist.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('genres',)
    http_method_names = ('get',)

    def get_serializer_class(self):
        if getattr(self, 'action', None) == 'list':
            return ArtistShortInfoSerializer
        return ArtistSerializer
