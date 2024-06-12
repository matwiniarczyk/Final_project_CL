import pytest


@pytest.fixture
def user_data():
    return {
        'username': 'test_user',
        'password': 'test',
        'password2': 'test',
    }


@pytest.fixture
def invalid_user_data():
    return {
        'username': 'test_user',
        'password': 'test',
        'password2': 'test_2',
    }


@pytest.fixture
def login_data():
    return {
        'username': 'Mateusz Winiarczyk',
        'password': 'dupa',
    }
