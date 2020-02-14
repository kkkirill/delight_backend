from rest_framework import generics
from apps.media.serializers.genre import GenreDetailSerializer
from apps.media.models.genre import Genre


class GenreCreateView(generics.CreateAPIView):
    serializer_class = GenreDetailSerializer


class GenreListView(generics.ListAPIView):
    serializer_class = GenreDetailSerializer
    queryset = Genre.objects.all()


class GenreUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GenreDetailSerializer
    queryset = Genre.objects.all()
