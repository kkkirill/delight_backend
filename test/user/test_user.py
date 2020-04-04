import json

import faker
import pytest


@pytest.mark.django_db
class TestUser:
    def test_login(self, client, user, token):
        """
        test user login
        """
        data = {
            "username": user.username,
            "password": 'password'
        }
        res = client.post(f'/auth/login/', data=data,
                          content_type="application/json")
        user_dict = res.json()
        assert res.status_code == 200
        assert user_dict.get('id') == user.id
        assert user_dict.get('token') == str(token)
        res = client.get(f'/auth/me/', content_type="application/json",
                         **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        user_dict = res.json()
        assert user_dict.get('email') == user.email
        assert user_dict.get('username') == user.username

    def test_about(self, client, user, token):
        """
        test user /me endpoint
        """
        res = client.get(f'/auth/me/', content_type="application/json",
                         **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        user_dict = res.json()
        assert res.status_code == 200
        assert user_dict.get('email') == user.email
        assert user_dict.get('username') == user.username
        assert isinstance(user_dict.get('photo'), str)
        assert isinstance(user_dict.get('followers'), list)
        assert isinstance(user_dict.get('followers_amount'), int)
        assert isinstance(user_dict.get('is_staff'), bool)

    def test_logout(self, client, user, token):
        """
        test user logout
        """
        res = client.post(f'/auth/logout/', content_type="application/json",
                          **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        user_dict = res.json()
        assert res.status_code == 200
        assert user_dict.get('details') == 'Logged out successfully'
        res = client.get(f'/auth/me/', content_type="application/json",
                         **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        assert res.status_code == 401

    def test_registration(self, client):
        """
        test user registration
        """
        username = faker.Faker().pystr(min_chars=5, max_chars=20)
        email = faker.Faker().email()
        password = faker.Faker().password(special_chars=False)
        data = json.dumps({
            "email": email,
            "username": username,
            "password": password
        })
        res = client.post(f'/auth/registration/', data=data,
                          content_type="application/json")
        user_dict = res.json()
        assert res.status_code == 201
        assert user_dict.get("email") == email
        assert user_dict.get("username") == username
