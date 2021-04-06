from drf_haystack.serializers import HaystackSerializer

from apps.search.indexes.song import SongIndex

from apps.search.indexes.artist import ArtistIndex

from apps.search.indexes.album import AlbumIndex


class CommonSearchSerializer(HaystackSerializer):
    class Meta:
        index_classes = [SongIndex, ArtistIndex, AlbumIndex]
        fields = [
            'title',
            'stage_name',
            'image',
            'photo',
            'file',
            'artists',
            'genres',
        ]
