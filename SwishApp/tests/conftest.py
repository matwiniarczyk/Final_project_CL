import pytest

from SwishApp.models import Court, Sport


@pytest.fixture
def court_data():
    basketball = Sport.objects.create(name='Basketball')
    test_court_1 = Court.objects.create(location="location_1")
    test_court_2 = Court.objects.create(location="location_2")
    test_court_1.intended_for.set([basketball])
    test_court_2.intended_for.set([basketball])
    return {'location': 'location_1', 'intended_for': basketball.id}
    # używamy id sportu, aby zachować spójność z form POST


@pytest.fixture
def invalid_court_data():
    basketball = Sport.objects.create(name='Basketball')
    test_court = Court.objects.create(location="")
    test_court.intended_for.set([basketball])
    return {'location': '', 'intended_for': basketball.id}
