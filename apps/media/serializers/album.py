from rest_framework.serializers import ModelSerializer

from apps.media.models.album import Album
from apps.media.models.artist import Artist
from apps.media.models.genre import Genre
from apps.media.models.song import Song
from apps.media.serializers.artist import ArtistShortInfoSerializer
from apps.media.serializers.genre import GenreDetailSerializer
from apps.media.serializers.song import SongShortInfoSerializer


class AlbumSerializer(ModelSerializer):
    genres = GenreDetailSerializer(many=True,)
    songs = SongShortInfoSerializer(many=True,)
    artists = ArtistShortInfoSerializer(many=True, )

    class Meta:
        model = Album
        fields = ('url', 'title', 'songs_amount', 'photo',
                  'release_year', 'artists', 'genres', 'songs')
        read_only_fields = ('songs_amount',)

    def create(self, validated_data):
        genres_data = validated_data.pop('genres')
        artists_data = validated_data.pop('artists')
        songs_data = validated_data.pop('songs')
        album = Album.objects.create(**validated_data)
        for genre_data in genres_data:
            album.genres.add(Genre.objects.get(**genre_data))
        for artist_data in artists_data:
            album.artists.add(Artist.objects.get(**artist_data))
        for song_data in songs_data:
            album.songs.add(Song.objects.get(**song_data))
        return album

    def update(self, instance, validated_data):
        genres_data = validated_data.pop('genres')
        artists_data = validated_data.pop('artists')
        songs_data = validated_data.pop('songs')
        instance.title = validated_data.get('title',
                                            instance.title)
        instance.songs_amount = validated_data.get('songs_amount', instance.songs_amount)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.release_year = validated_data.get('release_year', instance.release_year)
        instance.save()
        instance.genres.clear()
        instance.artists.clear()
        instance.songs.clear()
        for genre_data in genres_data:
            instance.genres.add(Genre.objects.get(**genre_data))
        for artist_data in artists_data:
            instance.artists.add(Artist.objects.get(**artist_data))
        for song_data in songs_data:
            instance.songs.add(Song.objects.get(**song_data))
        return instance


class AlbumShortInfoSerializer(AlbumSerializer):
    class Meta(AlbumSerializer.Meta):
        fields = ('url', 'title', 'photo', 'artists')
