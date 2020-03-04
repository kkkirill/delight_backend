from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter

from apps.media.models.album import Album
from apps.media.serializers.album import (
    AlbumSerializer, AlbumShortInfoSerializer)


class AlbumListView(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('genres', 'artists')
    ordering_fields = ('release_year',)
    http_method_names = ('get',)

    def get_serializer_class(self):
        if getattr(self, 'action', None) == 'list':
            return AlbumShortInfoSerializer
        return AlbumSerializer
