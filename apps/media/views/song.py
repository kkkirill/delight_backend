from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from apps.media.models.song import Song
from apps.media.serializers.song import SongDetailSerializer


class SongListView(viewsets.ReadOnlyModelViewSet):
    serializer_class = SongDetailSerializer
    queryset = Song.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('genres', 'artists', )
