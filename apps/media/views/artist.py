from rest_framework import viewsets
from apps.media.serializers.artist import ArtistDetailSerializer
from apps.media.models.artist import Artist
from django_filters.rest_framework import DjangoFilterBackend


class ArtistListView(viewsets.ReadOnlyModelViewSet):
    serializer_class = ArtistDetailSerializer
    queryset = Artist.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['genre']
