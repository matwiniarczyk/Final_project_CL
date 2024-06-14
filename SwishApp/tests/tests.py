import pytest
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase, Client
from django.urls import reverse

from SwishApp.forms import SearchCourtForm, AddCourtForm
from SwishApp.models import Court, Match


# TESTY WYSZUKIWANIA BOISK
@pytest.mark.django_db
def test_search_court_get():
    url = reverse('search_court')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], SearchCourtForm)
    # dodatkowo sprawdzamy, czy przekazany do kontekstu formularz należy do klasy SearchCourtForm


@pytest.mark.django_db
def test_search_court_post(court_data):
    url = reverse('search_court')
    client = Client()
    response = client.post(url, court_data)
    assert response.status_code == 200
    assert 'searched_courts' in response.context  # sprawdzamy, czy searched_courts przekazuje się do templaty
    searched_courts = response.context['searched_courts']  # bierzemy tego searched_courts z kontekstu i sprawdzamy...
    assert searched_courts is not None
    assert len(searched_courts) > 0
    assert searched_courts[0].location == court_data['location']
    # sprawdzamy, czy location w pierwszym przekazanym court to location naszego testu


@pytest.mark.django_db
def test_search_court_post_invalid_data(invalid_court_data):
    url = reverse('search_court')
    client = Client()
    response = client.post(url, invalid_court_data)
    assert response.status_code == 200
    assert 'form' in response.context  # sprawdzamy, czy formularz przekazuje się do templaty
    form = response.context['form']  # bierzemy ten formularz i sprawdzamy, czy wyrzuca błędy (puste pole location)
    assert form.errors


@pytest.mark.django_db
def test_search_court_post_no_results(no_matching_court):
    url = reverse('search_court')
    client = Client()
    response = client.post(url, no_matching_court)
    assert response.status_code == 200
    assert 'searched_courts' not in response.context
    assert 'form' not in response.context
    assert 'swishapp/no_matching_courts.html' in response.templates[0].name
    # response.templates to lista a pierwszy z jej elementów to zazwyczaj szablon użyty do wygenerowania odpowiedzi


# TESTY DODAWANIA BOISK
@pytest.mark.django_db
def test_add_court_get(court_data):
    url = reverse('add_court')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], AddCourtForm)


@pytest.mark.django_db
def test_add_court_post(court_data):
    url = reverse('add_court')
    client = Client()
    response = client.post(url, court_data)
    assert response.status_code == 302
    assert Court.objects.filter(name=court_data['name']).exists()


@pytest.mark.django_db
def test_add_court_post_invalid_data(invalid_court_data):
    url = reverse('add_court')
    client = Client()
    response = client.post(url, invalid_court_data)
    assert response.status_code == 200
    assert 'form' in response.context
    form = response.context['form']
    assert form.errors


# TEST LISTY BOISK
@pytest.mark.django_db
def test_court_list_get(court_list):
    url = reverse('court_list')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['courts'].count() == len(court_list)
    for court in court_list:
        assert court in response.context['courts']


# TEST WIDOKU SZCZEGÓŁOWEGO BOISK
@pytest.mark.django_db
def test_court_detail_get(court_matches):
    court, matches = court_matches
    url = reverse('court_detail', kwargs={'pk': court.id})
    client = Client()
    response = client.get(url)
    assert response.status_code == 200
    assert 'court' in response.context
    assert 'matches' in response.context
    assert response.context['court'] == court
    assert list(response.context['matches']) == list(court.match_set.all())
    assert court.name in str(response.content)
    for match in matches:
        assert match.get_day_display() in str(response.content)


# TESTY DODAWANIA MECZU
@pytest.mark.django_db
def test_add_match_get():
    court = Court.objects.create()
    url = reverse('add_match', kwargs={'pk': court.id})
    client = Client()
    user = User.objects.create_user(username='test', password='test')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    assert 'court' in response.context
    assert 'day_choices' in response.context
    assert 'time_choices' in response.context
    assert 'sports' in response.context


@pytest.mark.django_db
def test_add_match_post(match_data):
    url = reverse('add_match', kwargs={'pk': match_data['court']})
    client = Client()
    user = User.objects.create_user(username='test', password='test')
    client.force_login(user)
    response = client.post(url, match_data)
    assert response.status_code == 302
    assert Match.objects.filter(day=match_data['day'], time=match_data['time']).exists()
    messages = list(get_messages(response.wsgi_request))
    # response.wsgi_request to obiekt żądania HTTP, do którego jest przypisana odpowiedź response
    assert len(messages) == 1
    assert messages[0].tags == 'success'
    assert messages[0].message == 'Match added'
    # --------------------------------------#

    # response = client.post(url, match_data)
    # assert response.status_code == 302
    # messages = list(get_messages(response.wsgi_request))
    # assert len(messages) == 2
    # assert messages[0].tags == 'error'
    # assert messages[0].message == 'This match already exists'


# TEST LISTY MECZÓW
@pytest.mark.django_db
def test_matches_list_get(matches_list):
    matches, court = matches_list
    url = reverse('matches_list', kwargs={'pk': court.id})
    client = Client()
    response = client.get(url)
    assert response.status_code == 200
    assert 'court' in response.context
    assert response.context['court'] == court
    assert response.context['matches'].count() == len(matches)
    for match in matches:
        assert match in response.context['matches']
