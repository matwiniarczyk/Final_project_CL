from django.urls import path

from SwishApp import views

urlpatterns = [
    path('search_court/', views.SearchCourtView.as_view(), name='search_court'),
    path('add_court/', views.AddCourtView.as_view(), name='add_court'),
    path('court_list/', views.CourtListView.as_view(), name='court_list'),
    path('court_detail/<int:pk>/', views.CourtDetailView.as_view(), name='court_detail'),
    path('add_match/<int:pk>/', views.AddMatchView.as_view(), name='add_match'),
    path('matches_list/<int:pk>/', views.MatchesListView.as_view(), name='matches_list'),
]
