import pytest


@pytest.mark.django_db
class TestLikes:
    @pytest.mark.parametrize('content_type', ['song', 'album', 'artist'])
    def test_like_obj(self, client, user, token, content_type,
                      content_obj):
        """
        test like obj, test multiple like return 409 HTTP status
        """
        res = client.post(
            f'/api/{content_type}/{content_obj.id}/like/',
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'Token ' + str(token)}
        )
        assert res.status_code == 200
        res = client.post(
            f'/api/{content_type}/{content_obj.id}/like/',
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'Token ' + str(token)}
        )
        assert res.status_code == 409

    def test_remove_like(self, client, liked_song, user, song, token):
        """
        test remove like from song
        """
        res = client.get(
            f'/api/song/{song.id}/fans/',
            content_type='application/json'
        )
        fans_dict = res.json()[0]
        assert user.id == fans_dict['id']
        assert user.username == fans_dict['username']
        res = client.delete(
            f'/api/song/{song.id}/like/',
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'Token ' + str(token)}
        )
        assert res.status_code == 200
        res = client.get(
            f'/api/song/{song.id}/fans/',
            content_type='application/json'
        )
        fans_dict = res.json()
        assert len(fans_dict) == 0

    def test_like_auth_error(self, client, song):
        """
        test like song without auth
        """
        res = client.post(
            f'/api/song/{song.id}/like/',
            content_type='application/json',
        )
        assert res.status_code == 401
        response = res.json()['detail']
        assert response == 'Authentication credentials were not provided.'

    def test_unlike_error(self, client, song, user, token):
        """
        test remove not given like return 404 HTTP status
        """
        res = client.delete(
            f'/api/song/{song.id}/like/',
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'Token ' + str(token)}
        )
        assert res.status_code == 404

    @pytest.mark.parametrize('content_type', ['song', 'album', 'artist'])
    def test_get_fans(self, client, user, token, content_type,
                      content_obj):
        """
        test get fans endpoint
        """
        res = client.post(
            f'/api/{content_type}/{content_obj.id}/like/',
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'Token ' + str(token)}
        )
        assert res.status_code == 200
        res = client.get(
            f'/api/{content_type}/{content_obj.id}/fans/',
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'Token ' + str(token)}
        )
        assert res.status_code == 200
        fans_dict = res.json()[0]
        assert user.id == fans_dict['id']
        assert user.username == fans_dict['username']
