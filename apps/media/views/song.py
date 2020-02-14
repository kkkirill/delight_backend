from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.parsers import FileUploadParser, MultiPartParser

from apps.media.models.song import Song
from apps.media.serializers.song import SongDetailSerializer


# class ImageUploadParser(FileUploadParser):
#     media_type = 'image/*'
#
#
# class SongUploadParser(FileUploadParser):
#     media_type = 'audio/*'


class SongCreateView(generics.CreateAPIView):
    serializer_class = SongDetailSerializer
    # parser_classes = (MultiPartParser, )
    # parser_classes = (SongUploadParser, ImageUploadParser, )


class SongListView(generics.ListAPIView):
    serializer_class = SongDetailSerializer
    queryset = Song.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('genres', 'artists', )


class SongUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SongDetailSerializer
    queryset = Song.objects.all()
