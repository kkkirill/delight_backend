import json

import faker
import pytest


@pytest.mark.django_db
class TestPost:
    def test_detail(self, client, post, user):
        """
        test post detail
        """
        res = client.get(f'/api/user/{user.id}/post/{post.id}/',
                         content_type='application/json')
        data = res.json()

        assert res.status_code == 200
        assert isinstance(data.get('id'), int)
        assert isinstance(data.get('owner'), dict)
        assert isinstance(data.get('pubDate'), str)
        assert isinstance(data.get('totalLikes'), int)
        assert isinstance(data.get('text'), str)
        assert isinstance(data.get('images'), list)
        assert isinstance(data.get('songs'), list)
        assert isinstance(data.get('playlists'), list)
        assert isinstance(data.get('albums'), list)

    @pytest.mark.parametrize('is_staff', [True])
    @pytest.mark.parametrize('post_qty', [0, 5, 10, 25, 45])
    def test_list(self, client, user, token, posts, post_qty, is_staff):
        """
        test list of post on getting right:
            * amount
            * data type
        """
        res = client.get(f'/api/user/{user.id}/post/',
                         content_type='application/json',
                         **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        data = res.json()
        assert res.status_code == 200
        assert isinstance(data.get('results'), list)
        assert len(data.get('results')) == post_qty

    def test_create(self, client, user, token, post, post_images, songs, albums, playlists):
        """
        test create post
        """
        text = faker.Faker().pystr(min_chars=10, max_chars=30)
        songs = [song.id for song in songs]
        print(songs)
        albums = [album.id for album in albums]
        print(albums)
        playlists = [playlist.id for playlist in playlists]
        print(playlists)
        data = json.dumps({
            'text': text,
            'owner': user.id,
            'images': post_images,
            'songs': songs,
            'albums': albums,
            'playlists': playlists
        })
        res = client.post(f'/api/user/{user.id}/post/', data=data,
                          content_type='application/json',
                          **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        data = res.json()
        assert res.status_code == 201
        assert data.get('text') == text
        assert set(data.get('images')) == set(post_images)
        assert set(data.get('songs')) == set(songs)
        assert set(data.get('albums')) == set(albums)
        assert set(data.get('playlists')) == set(playlists)

