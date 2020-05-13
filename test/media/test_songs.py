import json

import faker
import pytest


@pytest.mark.django_db
class TestSongs:
    def test_detail(self, client, song):
        """
        test song details
            * check basic structure
        """
        res = client.get(f'/api/song/{song.id}/')
        song_dict = res.json()
        assert res.status_code == 200
        assert isinstance(song_dict.get('title'), str)
        assert isinstance(song_dict.get('duration'), int)
        assert isinstance(song_dict.get('image'), str)
        assert isinstance(song_dict.get('file'), str)
        assert isinstance(song_dict.get('listens'), int)
        assert isinstance(song_dict.get('artists'), list)
        assert isinstance(song_dict.get('genres'), list)
        assert song_dict.get('explicit') in (True, False)

    @pytest.mark.parametrize('song_qty', [0, 5, 10, 25, 45])
    def test_list(self, client, songs, song_qty):
        """
        test list of songs on getting right:
            * amount
            * data type
        """
        res = client.get('/api/song/')
        data = res.json()

        assert res.status_code == 200
        assert isinstance(data.get('results'), list)
        assert len(data.get('results')) == song_qty

    def test_detail_error(self, client):
        """
        test song details for non-existing song
        """
        res = client.get(
            f'/api/song/{faker.Faker().random_number(digits=30)}/')
        assert res.status_code == 404

    @pytest.mark.parametrize('is_staff', [True])
    def test_listen(self, client, song, token, user, redis, is_staff):
        """
        test song/:song_id/listen endpoint
        """
        factory = faker.Faker()
        title = song.title
        duration = song.duration

        start_second = factory.pyint(min_value=0, max_value=duration - 1)
        end_second = factory.pyint(min_value=start_second + 1,
                                   max_value=factory.pyint(
                                       min_value=start_second + 1,
                                       max_value=min(start_second + 30,
                                                     duration)))

        data = {
            'startSecond': start_second,
            'endSecond': end_second
        }
        data = json.dumps(data)
        res = client.post(f'/api/song/{song.id}/listen/', data=data,
                          content_type='application/json',
                          **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})

        song_dict = res.json()
        assert res.status_code == 200
        assert song_dict.get('title') == title
        assert song_dict.get('duration') == duration
        assert redis.smembers(f'{user.id}-{song.id}-piece') == {
            f'{start_second}-{end_second}'.encode()
        }

    @pytest.mark.parametrize('is_staff', [True])
    def test_create(self, client, artists_for_added, genres, token, user, is_staff):
        """
        test song create endpoint
        """
        factory = faker.Faker()
        title = factory.pystr(min_chars=5, max_chars=15)
        explicit = factory.pybool()
        file = factory.url(schemes=None) + factory.file_name(category='audio',
                                                             extension='mp3')
        image = factory.url(schemes=None) + factory.file_name(category='image',
                                                              extension='png')
        genres = [genre.id for genre in genres]
        artists = [artist.id for artist in artists_for_added]
        data = json.dumps({
            'title': title,
            'explicit': explicit,
            'image': image,
            'file': file,
            'genres': genres,
            'artists': artists
        })
        res = client.post('/api/song/', data=data,
                          content_type='application/json',
                          **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        song_dict = res.json()
        assert res.status_code == 201
        assert song_dict.get('title') == title
        assert song_dict.get('image') == image
        assert song_dict.get('file') == file
        assert song_dict.get('explicit') == explicit
        assert set(song_dict.get('genres')) == set(genres)
        assert set(song_dict.get('artists')) == set(artists)

    @pytest.mark.parametrize('is_staff', [True])
    def test_update_m2m(self, client, song, genres, token, user, is_staff):
        """
        test song update m2m field genres
        """
        title = faker.Faker().pystr(min_chars=5, max_chars=15)
        genres = [genre.id for genre in genres]
        data = json.dumps({
            'genres': genres,
            'title': title
        })
        res = client.put(f'/api/song/{song.id}/', data=data,
                         content_type='application/json',
                         **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        song_dict = res.json()
        assert res.status_code == 200
        assert song_dict.get('title') == title
        assert set(song_dict.get('genres')) == set(genres)

    @pytest.mark.parametrize('is_staff', [True])
    def test_update_all(self, client, song, genres, artists_for_added, token,
                        user, is_staff):
        """
        test artist update all fields
        """
        factory = faker.Faker()
        title = factory.pystr(min_chars=5, max_chars=15)
        explicit = factory.pybool()
        file = factory.url(schemes=None) + factory.file_name(category='audio',
                                                             extension='mp3')
        image = factory.url(schemes=None) + factory.file_name(category='image',
                                                              extension='png')
        genres = [genre.id for genre in genres]
        artists = [artist.id for artist in artists_for_added]
        data = json.dumps({
            'title': title,
            'explicit': explicit,
            'image': image,
            'file': file,
            'genres': genres,
            'artists': artists
        })
        res = client.put(f'/api/song/{song.id}/', data=data,
                         content_type='application/json',
                         **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        song_dict = res.json()
        assert res.status_code == 200
        assert song_dict.get('title') == title
        assert song_dict.get('image') == image
        assert song_dict.get('file') == file
        assert song_dict.get('explicit') == explicit
        assert set(song_dict.get('genres')) == set(genres)
        assert set(song_dict.get('artists')) == set(artists)
