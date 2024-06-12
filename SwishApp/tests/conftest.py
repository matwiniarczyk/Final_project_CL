import pytest

from SwishApp.models import Court, Sport


@pytest.fixture
def court_data():
    test_sport = Sport.objects.create(name='test_sport')
    test_court_1 = Court.objects.create(location="location")
    test_court_1.intended_for.set([test_sport])
    return {'name': 'test_name',
            'location': 'location',
            'intended_for': test_sport.id}
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
