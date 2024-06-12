import pytest
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from SwishApp.forms import SearchCourtForm, AddCourtForm
from SwishApp.models import Court


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
