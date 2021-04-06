from apps.media.serializers.song import SongShortInfoSerializer
from drf_haystack.serializers import HaystackSerializerMixin


class SongSearchSerializer(HaystackSerializerMixin, SongShortInfoSerializer):
    class Meta(SongShortInfoSerializer.Meta):
        pass
