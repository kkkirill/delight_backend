import json

import faker
import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import serializers
from rest_framework.parsers import FileUploadParser


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
        assert res.status_code == 200
        assert isinstance(res.json(), list)
        assert len(res.json()) == song_qty

    def test_detail_error(self, client):
        """
        test song details for non-existing song
        """
        res = client.get(f'/api/song/{faker.Faker().random_number(digits=30)}/')
        assert res.status_code == 404

    # def test_create(self, client, artists, genres):
    #     """
    #     test song create endpoint
    #     """
    #     title = faker.Faker().pystr(min_chars=5, max_chars=15)
    #     duration = faker.Faker().pyint(min_value=50)
    #     file = SimpleUploadedFile('song.mp3', b'song')
    #     explicit = faker.Faker().pybool()
    #     genres = [genre.id for genre in genres]
    #     artists = [artist.id for artist in artists]
    #     data = {
    #         'title': title,
    #         'duration': duration,
    #         'explicit': explicit,
    #         'file': file,
    #         'genres': genres,
    #         'artists': artists
    #     }
    #     data = json.dumps(data)
    #     res = client.post('/api/song/', data=data,
    #                       content_type="application/json")
    #     artist_dict = res.json()
    #     assert res.status_code == 201
    #     assert artist_dict.get("title") == title
    #     assert artist_dict.get("duration") == duration
    #     assert artist_dict.get("file") == file
    #     assert artist_dict.get("explicit") == explicit
    #     assert artist_dict.get("genres") == genres
    #     assert artist_dict.get("artists") == artists
    # 
    # def test_update_m2m(self, client, song, genres):
    #     """
    #     test song update m2m field genres
    #     """
    #     title = faker.Faker().pystr(min_chars=5, max_chars=15)
    #     genres = [genre.id for genre in genres]
    #     data = {"genres": genres, "title": title}
    #     data = json.dumps(data)
    #     res = client.put(f'/api/song/{song.id}/', data=data,
    #                      content_type="application/json")
    #     artist_dict = res.json()
    #     assert res.status_code == 200
    #     assert artist_dict.get("title") == title
    #     assert artist_dict.get("genres") == genres
    # 
    # def test_update_all(self, client, song, artists, genres):
    #     class FileSerializer(serializers.Serializer):
    #         file = serializers.FileField()
    #     """
    #     test song update all fields
    #     """
    #     title = faker.Faker().pystr(min_chars=5, max_chars=15)
    #     duration = faker.Faker().pyint(min_value=50)
    #     file = str(SimpleUploadedFile('song.mp3', b'song'))
    #     explicit = faker.Faker().pybool()
    #     genres = [genre.id for genre in genres]
    #     artists = [artist.id for artist in artists]
    #     data = {
    #         'title': title,
    #         'duration': duration,
    #         'explicit': explicit,
    #         'file': file,
    #         'genres': genres,
    #         'artists': artists
    #     }
    #     data = json.dumps(data)
    #     res = client.put(f'/api/song/{song.id}/', data=data,
    #                      content_type="application/json")
    #     artist_dict = res.json()
    #     assert res.status_code == 200
    #     assert artist_dict.get("title") == title
    #     assert artist_dict.get("duration") == duration
    #     assert artist_dict.get("file") == str(file)
    #     assert artist_dict.get("explicit") == explicit
    #     assert artist_dict.get("genres") == genres
    #     assert artist_dict.get("artists") == artists
