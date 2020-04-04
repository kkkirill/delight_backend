import json

import faker
import pytest


@pytest.mark.django_db
class TestArtists:
    def test_detail(self, client, artist):
        """
        test artist details
            * check basic structure
        """
        res = client.get(f'/api/artist/{artist.id}/')
        artist_dict = res.json()
        assert res.status_code == 200
        assert isinstance(artist_dict.get('stage_name'), str)
        assert isinstance(artist_dict.get('info'), str)
        assert isinstance(artist_dict.get('photo'), str)
        assert isinstance(artist_dict.get('genres'), list)

    @pytest.mark.parametrize('artist_qty', [0, 5, 10, 25, 45])
    def test_list(self, client, artists, artist_qty):
        """
        test list of artists on getting right:
            * amount
            * data type
        """
        res = client.get('/api/artist/')
        assert res.status_code == 200
        assert isinstance(res.json(), list)
        assert len(res.json()) == artist_qty

    def test_detail_error(self, client):
        """
        test artist details for non-existing artist
        """
        res = client.get(f'/api/artist/{faker.Faker().random_number(digits=30)}/')
        assert res.status_code == 404

    @pytest.mark.parametrize('is_staff', [True])
    def test_create(self, client, genres, user, token):
        """
        test artist create endpoint
        """
        stage_name = faker.Faker().name()
        genres = [genre.id for genre in genres]
        data = json.dumps({
            "stage_name": stage_name,
            "genres": genres
        })
        res = client.post('/api/artist/', data=data,
                          content_type="application/json",
                          **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        artist_dict = res.json()
        assert res.status_code == 201
        assert set(artist_dict.get("genres")) == set(genres)
        assert artist_dict.get("stage_name") == stage_name

    @pytest.mark.parametrize('is_staff', [True])
    def test_update_m2m(self, client, artist, genres, user, token):
        """
        test artist update m2m field genres
        """
        info = faker.Faker().pystr(min_chars=20, max_chars=300)
        genres = [genre.id for genre in genres]
        data = json.dumps({
            "genres": genres,
            "info": info
        })
        res = client.put(f'/api/artist/{artist.id}/', data=data,
                         content_type="application/json",
                         **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        artist_dict = res.json()
        assert res.status_code == 200
        assert artist_dict.get("info") == info
        assert set(artist_dict.get("genres")) == set(genres)

    @pytest.mark.parametrize('is_staff', [True])
    def test_update_all(self, client, artist, genres, user, token):
        """
        test artist update all fields
        """
        stage_name = faker.Faker().name()
        genres = [genre.id for genre in genres]
        info = faker.Faker().pystr(min_chars=20, max_chars=300)
        data = json.dumps({
            "stage_name": stage_name,
            "genres": genres,
            "info": info
        })
        res = client.put(f'/api/artist/{artist.id}/', data=data,
                         content_type="application/json",
                         **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        artist_dict = res.json()
        assert res.status_code == 200
        assert artist_dict.get("info") == info
        assert set(artist_dict.get("genres")) == set(genres)
        assert artist_dict.get("stage_name") == stage_name
