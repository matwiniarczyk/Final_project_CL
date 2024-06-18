import pytest
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse


def test_base_view():
    url = reverse('base')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200


# TESTY REGISTER, LOGIN, LOGOUT
def test_create_user_get():
    url = reverse('register')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_user_post(user_data):
    url = reverse('register')
    client = Client()
    response = client.post(url, user_data)
    assert response.status_code == 302
    assert settings.AUTH_USER_MODEL.objects.filter(username=user_data['username']).exists()


@pytest.mark.django_db
def test_create_user_invalid_data_post(invalid_user_data):
    url = reverse('register')
    client = Client()
    response = client.post(url, invalid_user_data)
    assert response.status_code == 200
    assert b'Passwords do not match, try again!' in response.content


def test_login():
    url = reverse('login')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_post(login_data):
    user = User.objects.create_user(username=login_data['username'], password=login_data['password'])
    url = reverse('login')
    client = Client()
    response = client.post(url, login_data)
    assert response.status_code == 302
    assert '_auth_user_id' in client.session    # sprawdzamy, czy identyfikator tego użytkownika widnieje w sesji


@pytest.mark.django_db
def test_logout(login_data):
    user = User.objects.create_user(username=login_data['username'], password=login_data['password'])
    url_logout = reverse('logout')
    url_login = reverse('login')
    client = Client()
    response = client.post(url_login, login_data)
    response = client.get(url_logout)
    assert response.status_code == 302
    assert '_auth_user_id' not in client.session
