from apps.media.serializers.artist import ArtistShortInfoSerializer
from drf_haystack.serializers import HaystackSerializerMixin


class ArtistSearchSerializer(HaystackSerializerMixin, ArtistShortInfoSerializer):
    class Meta(ArtistShortInfoSerializer.Meta):
        pass
