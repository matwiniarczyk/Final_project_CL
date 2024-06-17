import pytest
from django.contrib.auth.models import User, Permission

from SwishApp.models import Court, Sport, Match, Comment


@pytest.fixture
def user():
    return User.objects.create_superuser(username='test_user', password='test_password')


@pytest.fixture
def sport():
    return Sport.objects.create(name='test_sport')


@pytest.fixture
def court(sport):
    court = Court.objects.create(name='test_court', location='testlocation')
    court.intended_for.set([sport])
    return court


@pytest.fixture
def court_as_dict(sport):
    return {
        'name': 'test_court',
        'location': 'testlocation',
        'intended_for': sport.id,
    }


@pytest.fixture
def search_court(sport):
    test_court = Court.objects.create(name='test_court', location='testlocation')
    test_court.intended_for.set([sport])
    return {
        'location': 'testlocation',
        'intended_for': sport.id}


@pytest.fixture
def invalid_court_data(sport):
    return {'name': 'test_name',
            'location': '12345',
            'intended_for': sport}


@pytest.fixture
def no_matching_court(sport):
    test_court = Court.objects.create(name='test_court', location='testlocation')
    test_court.intended_for.set([sport])
    return {
        'name': 'test_name',
        'location': 'jydutyfbonoty',
        'intended_for': sport.id}


@pytest.fixture
def court_list(sport):
    lst = []
    for i in range(5):
        test_court = Court.objects.create(name=f'test_court_{i}', location=f'testlocation_{i}')
        test_court.intended_for.set([sport])
        lst.append(test_court)
    return lst


@pytest.fixture
def court_matches(user, sport, court):
    match_1 = Match.objects.create(day=1, time=1, added_by=user, sport=sport)
    match_1.court.set([court])
    match_2 = Match.objects.create(day=2, time=2, added_by=user, sport=sport)
    match_2.court.set([court])
    match_3 = Match.objects.create(day=3, time=3, added_by=user, sport=sport)
    match_3.court.set([court])
    return [match_1, match_2, match_3]


@pytest.fixture
def match_data(user, sport):
    test_court = Court.objects.create(name='test', location='test')
    test_court.intended_for.set([sport])
    return {'day': 1234,
            'time': 1234,
            'sport': sport.id,
            'added_by': user.id,
            'court': test_court.id}


@pytest.fixture
def matches_list(user, sport, court):
    lst = []
    for i in range(5):
        match = Match.objects.create(day=i, time=i, added_by=user, sport=sport)
        match.court.set([court])
        lst.append(match)
    return lst


@pytest.fixture
def update_court(sport):
    return {
        'name': 'update_name',
        'location': 'updatelocation',
        'intended_for': sport.id,
    }


@pytest.fixture
def comment(user, court):
    return Comment.objects.create(user=user, court=court, text='test comment')
