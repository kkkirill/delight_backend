from rest_framework import viewsets

from apps.media.models.genre import Genre
from apps.media.serializers.genre import GenreDetailSerializer


class GenreView(viewsets.ModelViewSet):
    serializer_class = GenreDetailSerializer
    queryset = Genre.objects.all()
    http_method_names = ('get',)
