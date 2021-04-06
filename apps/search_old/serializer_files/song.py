from apps.media.serializers.song import SongShortInfoSerializer


class SearchSongShortInfoSerializer(SongShortInfoSerializer):
    class Meta(SongShortInfoSerializer.Meta):
        fields = ('id', 'title', 'explicit', 'artists')


