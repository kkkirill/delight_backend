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
        assert res.status_code == 200
        assert isinstance(res.json(), list)
        assert len(res.json()) == song_qty

    def test_detail_error(self, client):
        """
        test song details for non-existing song
        """
        res = client.get(f'/api/song/{faker.Faker().random_number(digits=30)}/')
        assert res.status_code == 404
