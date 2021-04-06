from apps.media.serializers.album import AlbumShortInfoSerializer
from drf_haystack.serializers import HaystackSerializerMixin


class AlbumSearchSerializer(HaystackSerializerMixin, AlbumShortInfoSerializer):
    class Meta(AlbumShortInfoSerializer.Meta):
        pass
