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
        assert res.status_code == 200
        song_dict = res.json()
        fields = ('title', 'duration', 'image', 'file', 'listens', 'explicit', 'artists', 'genres')
        assert all(k in song_dict for k in fields)

    @pytest.mark.parametrize('song_qty', [0, 5, 10, 25, 45])
    def test_list(self, client, songs, song_qty):
        """
        test list of song on getting right:
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
