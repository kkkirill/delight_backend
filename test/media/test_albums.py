import json

import faker
import pytest


@pytest.mark.django_db
class TestAlbums:
    def test_detail(self, client, album):
        """
        test albums details
            * check basic structure
        """
        res = client.get(f'/api/album/{album.id}/')
        album_dict = res.json()
        assert res.status_code == 200
        assert isinstance(album_dict.get('title'), str)
        assert isinstance(album_dict.get('songsAmount'), int)
        assert isinstance(album_dict.get('photo'), str)
        assert isinstance(album_dict.get('releaseYear'), str)
        assert isinstance(album_dict.get('artists'), list)
        assert isinstance(album_dict.get('genres'), list)
        assert isinstance(album_dict.get('songs'), list)

    @pytest.mark.parametrize('album_qty', [0, 3, 5, 7, 10])
    def test_list(self, client, albums, album_qty):
        """
        test list of albums on getting right:
            * amount
            * data type
        """
        res = client.get('/api/album/')
        data = res.json()
        assert res.status_code == 200
        assert isinstance(data.get('results'), list)
        assert len(data.get('results')) == album_qty

    def test_detail_error(self, client):
        """
        test album details for non-existing album
        """
        res = client.get(
            f'api/album/{faker.Faker().random_number(digits=30)}/')

        assert res.status_code == 404

    @pytest.mark.parametrize('is_staff', [True])
    def test_create(self, client, genres, album, artists_for_added, token,
                    songs_for_added, user, is_staff):
        """
        test album create endpoint
        """
        title = faker.Faker().pystr(min_chars=10, max_chars=30)
        genres = [genre.id for genre in genres]
        artists = [artist.id for artist in artists_for_added]
        songs = [song.id for song in songs_for_added]
        release_year = faker.Faker().date()
        data = json.dumps({
            'title': title,
            'genres': genres,
            'artists': artists,
            'songs': songs,
            'releaseYear': release_year
        })
        res = client.post(f'/api/album/', data=data,
                          content_type='application/json',
                          **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        album_dict = res.json()
        assert res.status_code == 201
        assert album_dict.get('title') == title
        assert set(album_dict.get('genres')) == set(genres)
        assert set(album_dict.get('artists')) == set(artists)
        assert set(album_dict.get('songs')) == set(songs)
        assert album_dict.get('releaseYear') == release_year

    @pytest.mark.parametrize('is_staff', [True])
    def test_update_m2m(self, client, genres, album, artists_for_added, token,
                        songs_for_added, user, is_staff):
        """
        test album update m2m fields:
            *genres
            *artists
            *songs
        """
        title = faker.Faker().pystr(min_chars=10, max_chars=30)
        genres = [genre.id for genre in genres]
        artists = [artist.id for artist in artists_for_added]
        songs = [song.id for song in songs_for_added]
        data = json.dumps({
            'title': title,
            'genres': genres,
            'artists': artists,
            'songs': songs
        })
        res = client.put(f'/api/album/{album.id}/', data=data,
                         content_type='application/json',
                         **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        album_dict = res.json()
        assert res.status_code == 200
        assert album_dict.get('title') == title
        assert set(album_dict.get('genres')) == set(genres)
        assert set(album_dict.get('artists')) == set(artists)
        assert set(album_dict.get('songs')) == set(songs)

    @pytest.mark.parametrize('is_staff', [True])
    def test_update_all(self, client, genres, album, artists, songs_for_added,
                        token, user, is_staff):
        """
        test album update fields
        """
        title = faker.Faker().pystr(min_chars=10, max_chars=30)
        genres = [genre.id for genre in genres]
        artists = [artist.id for artist in artists]
        songs = [song.id for song in songs_for_added]
        release_year = faker.Faker().date()
        data = json.dumps({
            'title': title,
            'genres': genres,
            'artists': artists,
            'songs': songs,
            'releaseYear': release_year
        })
        res = client.put(f'/api/album/{album.id}/', data=data,
                         content_type='application/json',
                         **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        album_dict = res.json()
        assert res.status_code == 200
        assert album_dict.get('title') == title
        assert set(album_dict.get('genres')) == set(genres)
        assert set(album_dict.get('artists')) == set(artists)
        assert set(album_dict.get('songs')) == set(songs)
        assert album_dict.get('releaseYear') == release_year
