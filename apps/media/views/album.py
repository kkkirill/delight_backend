from rest_framework import generics
from apps.media.models.album import Album
from apps.media.serializers.album import AlbumSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


class AlbumCreateView(generics.CreateAPIView):
    serializer_class = AlbumSerializer
    queryset = Album.objects.all()


class AlbumListView(generics.ListAPIView):
    serializer_class = AlbumSerializer
    queryset = Album.objects.all()

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['genres', 'artists']
    ordering_fields = ['release_year']


class AlbumUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AlbumSerializer
    queryset = Album.objects.all()
