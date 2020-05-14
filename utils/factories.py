from random import randint
from typing import Union

import factory
from django.contrib.contenttypes.models import ContentType

from apps.likes.models.like import Like
from apps.media.models.album import Album
from apps.media.models.artist import Artist
from apps.media.models.genre import Genre
from apps.media.models.song import Song
from apps.user.models import Post
from apps.user.models.playlist import Playlist
from apps.user.models.user import User

factory.Faker._DEFAULT_LOCALE = 'ru_RU'

GENRES = [
    'Hip - Hop',
    'Reggae',
    'Pop',
    'Indie',
    'Rock',
    'Classic',
    'R & B',
    'Jazz',
]


class GenreFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: GENRES[n % len(GENRES)])

    class Meta:
        model = Genre


class ArtistFactory(factory.django.DjangoModelFactory):
    stage_name = factory.Faker('name')
    info = factory.Faker('text', max_nb_chars=200)
    photo = factory.Faker('image_url')

    class Meta:
        model = Artist

    @factory.post_generation
    def genres(self, create, extracted):
        if not create:
            return

        if extracted:
            for gn in extracted:
                self.genres.add(gn)


class SongFactory(factory.django.DjangoModelFactory):
    title = factory.Faker('pystr', min_chars=5, max_chars=15)
    duration = factory.Faker('pyint', min_value=30, max_value=300)
    file = factory.Faker('file_name', category="audio")
    image = factory.Faker('image_url')
    listens = factory.Faker('pyint')
    explicit = factory.Faker('pybool')

    class Meta:
        model = Song

    @factory.post_generation
    def artists(self, create, extracted):
        if not create:
            return

        if extracted:
            for ar in extracted:
                self.artists.add(ar)

    @factory.post_generation
    def genres(self, create, extracted):
        if not create:
            return

        if extracted:
            for gn in extracted:
                self.genres.add(gn)


class AlbumFactory(factory.django.DjangoModelFactory):
    title = factory.Faker('pystr', min_chars=5, max_chars=15)
    release_year = factory.Faker('date_between', start_date='-30y',
                                 end_date='now')
    photo = factory.Faker('image_url')

    class Meta:
        model = Album

    @factory.post_generation
    def artists(self, create, extracted):
        if not create:
            return

        if extracted:
            for ar in extracted:
                self.artists.add(ar)

    @factory.post_generation
    def genres(self, create, extracted):
        if not create:
            return

        if extracted:
            for gn in extracted:
                self.genres.add(gn)

    @factory.post_generation
    def songs(self, create, extracted):
        if not create:
            return

        if extracted:
            for so in extracted:
                self.songs.add(so)


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker('pystr', min_chars=5, max_chars=20)
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'password')
    photo = factory.Faker('image_url')
    followers_amount = 0
    is_staff = factory.Faker('pybool')

    class Meta:
        model = User

    @factory.post_generation
    def followers(self, create, extracted):
        if not create:
            return

        if extracted:
            self.followers_amount = len(extracted)

            for fo in extracted:
                self.followers.add(fo)


class PlaylistFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('pystr', min_chars=5, max_chars=10)
    is_private = factory.Faker('pybool')
    photo = factory.Faker('image_url')
    owner = factory.SubFactory(UserFactory)

    class Meta:
        model = Playlist

    @factory.post_generation
    def songs(self, create, extracted):
        if not create:
            return

        if extracted:
            for so in extracted:
                self.songs.add(so)


class PostFactory(factory.django.DjangoModelFactory):
    owner = factory.SubFactory(UserFactory)
    text = factory.Faker('pystr', min_chars=5, max_chars=50)
    images = [factory.Faker('image_url').generate() for i in range(randint(1, 11))]
    pub_date = factory.Faker('date_time')

    class Meta:
        model = Post

    @factory.post_generation
    def songs(self, create, extracted):
        if not create:
            return

        if extracted:
            for so in extracted:
                self.songs.add(so)

    @factory.post_generation
    def albums(self, create, extracted):
        if not create:
            return

        if extracted:
            for ar in extracted:
                self.albums.add(ar)

    @factory.post_generation
    def playlists(self, create, extracted):
        if not create:
            return

        if extracted:
            for ar in extracted:
                self.playlists.add(ar)


class LikedObjectFactory(factory.django.DjangoModelFactory):
    object_id = factory.SelfAttribute('content_object.id')
    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.content_object))

    class Meta:
        exclude = ['content_object']
        abstract = True


class LikedArtistFactory(LikedObjectFactory):
    content_object = Artist

    class Meta:
        model = Like


class LikedAlbumFactory(LikedObjectFactory):
    content_object = Album

    class Meta:
        model = Like


class LikedSongFactory(LikedObjectFactory):
    content_object = Song

    class Meta:
        model = Like


class LikedPlaylistFactory(LikedObjectFactory):
    content_object = Playlist

    class Meta:
        model = Like


class LikedPostFactory(LikedObjectFactory):
    content_object = Post

    class Meta:
        model = Like


def fill_with_data(model: Union[Album, Artist, Genre, Song, User, Playlist, Post],
                   min_limit: int, max_limit: int) -> frozenset:
    """
    This function generates a collection with random size.
        Takes:
            model: queryset with multiple instances of one type(
                Album, Artist, Genre, Song, Playlist or User
            ).
            min_limit: defines min size of collection, integer.
            max_limit: defines max size of collection, integer.
        Logic:
            Fills buffer with randomly chosen instances from model.
            Buffer size variates from min_limit to max_limit.
        Returns:
            Hashable buffer with random amount of model instances.
    """
    return frozenset(
        model[randint(0, len(model) - 1)]
        for _ in range(randint(min_limit, max_limit))
    )


def get_id(obj: frozenset) -> int:
    return set(obj).pop().id


def fill(amount=50):
    Album.objects.all().delete()
    Artist.objects.all().delete()
    Genre.objects.all().delete()
    Song.objects.all().delete()
    User.objects.all().delete()
    Playlist.objects.all().delete()
    Post.objects.all().delete()
    Like.objects.all().delete()

    # creating genres here
    for _ in range(len(GENRES)):
        GenreFactory.create()

    # creating artists here
    genres = Genre.objects.all()
    for _ in range(amount // 3):
        ArtistFactory.create(genres=fill_with_data(genres, 1, 3))

    # creating songs here
    artists = Artist.objects.all()
    for _ in range(amount):
        SongFactory.create(artists=fill_with_data(artists, 1, 3),
                           genres=fill_with_data(genres, 1, 3))

    # creating albums here
    songs = Song.objects.all()
    for _ in range(amount // 4):
        AlbumFactory.create(artists=fill_with_data(artists, 1, 3),
                            genres=fill_with_data(genres, 1, 3),
                            songs=fill_with_data(songs, 5, 10))

    # creating users here
    albums = Album.objects.all()
    for _ in range(amount):
        users = User.objects.all()
        user = UserFactory.create(
            followers=fill_with_data(users, 0, len(users) // 5)
        )
        PlaylistFactory.create(name='Favorites', is_private=True, owner=user)
        PlaylistFactory.create(name='My Songs', is_private=True, owner=user)
        # creating playlists and likes for user
        for _ in range(amount // 10):
            PlaylistFactory.create(
                songs=fill_with_data(songs, 5, 10),
                owner=user
            )
            LikedArtistFactory.create(
                user=user,
                object_id=get_id(fill_with_data(artists, 1, 1))
            )
            LikedAlbumFactory.create(
                user=user,
                object_id=get_id(fill_with_data(albums, 1, 1))
            )
            LikedSongFactory.create(
                user=user,
                object_id=get_id(fill_with_data(songs, 1, 1))
            )
        PostFactory.create(
            songs=fill_with_data(songs, 5, 10),
            albums=fill_with_data(albums, 5, 10),
            playlists=fill_with_data(Playlist.objects.filter(owner=user).all(), 5, 10)
        )

    # creating likes for playlists here
    User.objects.filter(playlists=None).delete()
    users = User.objects.all()
    playlists = Playlist.objects.all()
    for _ in range(amount // 10):
        for user in users:
            LikedPlaylistFactory.create(
                user=user,
                object_id=get_id(fill_with_data(playlists, 1, 1))
            )
