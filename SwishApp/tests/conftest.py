import pytest
from django.contrib.auth.models import User

from SwishApp.models import Court, Sport, Match


@pytest.fixture
def court_data():
    test_sport = Sport.objects.create(name='test_sport')
    test_court_1 = Court.objects.create(name='test', location="test")
    test_court_1.intended_for.set([test_sport])
    return {'name': test_court_1.name, 'location': test_court_1.location, 'intended_for': test_sport.id}
    # używamy id sportu, aby zachować spójność z form POST


@pytest.fixture
def invalid_court_data():
    test_sport = Sport.objects.create(name='test_sport')
    test_court = Court.objects.create()
    test_court.intended_for.set([test_sport])
    return {'name': 'test_name', 'location': '12345', 'intended_for': test_sport}


@pytest.fixture
def no_matching_court():
    test_sport = Sport.objects.create(name='dupa')
    test_court = Court.objects.create()
    test_court.intended_for.set([test_sport])
    return {'name': 'stygdgyurd', 'location': 'hgruivguvdfgvgui', 'intended_for': test_sport.id}


@pytest.fixture
def court_list():
    lst = []
    test_sport = Sport.objects.create(name='test_sport')
    for i in range(5):
        court = Court.objects.create(name='test', location='test')
        court.intended_for.set([test_sport])
        lst.append(court)
    return lst


@pytest.fixture
def court_matches():
    user = User.objects.create_user(username='test_user', password='test_password')
    test_sport = Sport.objects.create(name='test_sport')
    test_court = Court.objects.create(name='test', location='test')
    test_court.intended_for.set([test_sport])
    match_1 = Match.objects.create(day=1, time=1, added_by=user, sport=test_sport)
    match_1.court.set([test_court])
    match_2 = Match.objects.create(day=2, time=2, added_by=user, sport=test_sport)
    match_2.court.set([test_court])
    match_3 = Match.objects.create(day=3, time=3, added_by=user, sport=test_sport)
    match_3.court.set([test_court])
    return test_court, [match_1, match_2, match_3]


@pytest.fixture
def match_data():
    user = User.objects.create_user(username='test_user', password='test_password')
    test_sport = Sport.objects.create(name='test_sport')
    test_court = Court.objects.create(name='test', location='test')
    test_court.intended_for.set([test_sport])
    return {'day': 1234,
            'time': 1234,
            'sport': test_sport.id,
            'added_by': user.id,
            'court': test_court.id}


@pytest.fixture
def matches_list():
    lst = []
    user = User.objects.create_user(username='test_user', password='test')
    test_sport = Sport.objects.create(name='test_sport')
    test_court = Court.objects.create(name='test', location='test')
    test_court.intended_for.set([test_sport])
    for i in range(5):
        match = Match.objects.create(day=i, time=i, added_by=user, sport=test_sport)
        match.court.set([test_court])
        lst.append(match)
    return lst, test_court
