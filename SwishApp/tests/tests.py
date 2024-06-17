import pytest
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase, Client
from django.urls import reverse

from SwishApp.forms import SearchCourtForm, AddCourtForm, AddCommentForm
from SwishApp.models import Court, Match, Comment


# TESTY WYSZUKIWANIA BOISK
@pytest.mark.django_db
def test_search_court_get():
    url = reverse('search_court')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], SearchCourtForm)


@pytest.mark.django_db
def test_search_court_form_valid(sport, search_court):
    form = SearchCourtForm(search_court)
    assert form.is_valid()


@pytest.mark.django_db
def test_search_court_post(search_court):
    url = reverse('search_court')
    client = Client()
    response = client.post(url, search_court)
    assert response.status_code == 200
    assert 'swishapp/filtered_court_list.html' in response.templates[0].name
    assert 'searched_courts' in response.context
    searched_courts = response.context['searched_courts']
    assert searched_courts is not None
    assert len(searched_courts) > 0
    assert searched_courts[0].location == search_court['location']
    # sprawdzić intended_for


@pytest.mark.django_db
def test_search_court_post_invalid_data(invalid_court_data):
    url = reverse('search_court')
    client = Client()
    response = client.post(url, invalid_court_data)
    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], SearchCourtForm)


@pytest.mark.django_db
def test_search_court_post_no_results(no_matching_court):
    url = reverse('search_court')
    client = Client()
    response = client.post(url, no_matching_court)
    assert response.status_code == 200
    assert 'swishapp/no_matching_courts.html' in response.templates[0].name


# TESTY DODAWANIA BOISK
@pytest.mark.django_db
def test_add_court_get():
    url = reverse('add_court')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], AddCourtForm)


@pytest.mark.django_db
def test_add_court_post(court_as_dict):
    url = reverse('add_court')
    client = Client()
    response = client.post(url, court_as_dict)
    assert response.status_code == 302
    assert Court.objects.filter(name=court_as_dict['name']).exists()
    assert Court.objects.filter(location=court_as_dict['location']).exists()
    assert Court.objects.filter(intended_for=court_as_dict['intended_for']).exists()


@pytest.mark.django_db
def test_add_court_post_invalid_data(invalid_court_data):
    url = reverse('add_court')
    client = Client()
    response = client.post(url, invalid_court_data)
    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], AddCourtForm)


# TEST LISTY BOISK
@pytest.mark.django_db
def test_court_list_get(court_list):
    url = reverse('court_list')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['courts'].count() == len(court_list)
    for test_court in court_list:
        assert test_court in response.context['courts']


# TEST WIDOKU SZCZEGÓŁOWEGO BOISK
@pytest.mark.django_db
def test_court_detail_get(court_matches, court):
    url = reverse('court_detail', kwargs={'pk': court.id})
    client = Client()
    response = client.get(url)
    assert response.status_code == 200
    assert 'court' in response.context
    assert 'matches' in response.context
    assert response.context['court'] == court
    assert list(response.context['matches']) == list(court.match_set.all())
    assert court.name in str(response.content)
    for match in court_matches:
        assert match.get_day_display() in str(response.content)


# TESTY DODAWANIA MECZU
@pytest.mark.django_db
def test_add_match_get(court, user):
    url = reverse('add_match', kwargs={'pk': court.id})
    client = Client()
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    assert 'court' in response.context
    assert 'day_choices' in response.context
    assert 'time_choices' in response.context
    assert 'sports' in response.context


@pytest.mark.django_db
def test_add_match_post(match_data, user):
    url = reverse('add_match', kwargs={'pk': match_data['court']})
    client = Client()
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

    response = client.post(url, match_data)
    assert response.status_code == 302
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 2
    assert messages[1].tags == 'error'
    assert messages[1].message == 'This match already exists'


# TEST LISTY MECZÓW
@pytest.mark.django_db
def test_matches_list_get(court, matches_list):
    url = reverse('matches_list', kwargs={'pk': court.id})
    client = Client()
    response = client.get(url)
    assert response.status_code == 200
    assert 'court' in response.context
    assert response.context['court'] == court
    assert response.context['matches'].count() == len(matches_list)
    for match in matches_list:
        assert match in response.context['matches']


# TEST USUWANIA BOISKA
@pytest.mark.django_db
def test_delete_court_get(user, court):
    url = reverse('delete_court', kwargs={'pk': court.id})
    client = Client()
    client.force_login(user)
    assert Court.objects.filter(id=court.id).exists()
    response = client.delete(url)
    assert response.status_code == 302
    assert not Court.objects.filter(id=court.id).exists()


# TESTY UPDATE'OWANIA BOISKA
@pytest.mark.django_db
def test_update_court_get(user, court):
    url = reverse('update_court', kwargs={'pk': court.id})
    client = Client()
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    assert 'swishapp/update_court.html' in response.templates[0].name
    assert 'form' in response.context
    assert isinstance(response.context['form'], AddCourtForm)


@pytest.mark.django_db
def test_update_court_post(user, court, update_court):
    url = reverse('update_court', kwargs={'pk': court.id})
    client = Client()
    client.force_login(user)
    response = client.post(url, update_court)
    assert response.status_code == 302
    assert response.url == reverse('court_list')
    updated_court = Court.objects.get(id=court.id)
    assert updated_court.name == 'update_name'
    assert updated_court.location == 'updatelocation'


# TESTY DODAWANIA KOMENTARZA
@pytest.mark.django_db
def test_add_comment_get(user, court):
    url = reverse('court_comment', kwargs={'pk': court.id})
    client = Client()
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    assert 'swishapp/add_comment.html' in response.templates[0].name
    assert 'form' in response.context
    assert isinstance(response.context['form'], AddCommentForm)


@pytest.mark.django_db
def test_add_comment_post(user, court):
    url = reverse('court_comment', kwargs={'pk': court.id})
    client = Client()
    client.force_login(user)
    form_data = {'text': 'test comment by user'}
    response = client.post(url, form_data)
    assert response.status_code == 302
    assert court.comment_set.filter(text='test comment by user').exists()


# TESTY UPDATE'OWANIA KOMENTARZA
@pytest.mark.django_db
def test_update_comment_get(user, court, comment):
    url = reverse('update_comment', kwargs={'pk': comment.id})
    client = Client()
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context
    form = response.context['form']
    assert form.instance == comment


@pytest.mark.django_db
def test_update_comment_post(user, court, comment):
    url = reverse('update_comment', kwargs={'pk': comment.id})
    client = Client()
    client.force_login(user)
    form_data = {'text': 'update comment'}
    response = client.post(url, form_data)
    assert response.status_code == 302
    updated_comment = Comment.objects.get(id=comment.id)
    assert updated_comment.text == 'update comment'


@pytest.mark.django_db
def test_update_comment_post_unauthorized(user, comment):
    url = reverse('update_comment', kwargs={'pk': comment.id})
    client = Client()
    unauthorized_user = User.objects.create_user(username='unauthorized_user', password='test')
    client.force_login(unauthorized_user)
    form_data = {'text': 'update comment'}
    response = client.post(url, form_data)
    assert response.status_code == 403  # Forbidden
