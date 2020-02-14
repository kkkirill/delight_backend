from rest_framework import generics
from apps.media.serializers.artist import ArtistDetailSerializer
from apps.media.models.artist import Artist
from django_filters.rest_framework import DjangoFilterBackend


class ArtistCreateView(generics.CreateAPIView):
    serializer_class = ArtistDetailSerializer


class ArtistListView(generics.ListAPIView):
    serializer_class = ArtistDetailSerializer
    queryset = Artist.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['genre']


class ArtistUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ArtistDetailSerializer
    queryset = Artist.objects.all()
