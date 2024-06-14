from django.urls import path

from SwishApp import views

urlpatterns = [
    path('search_court/', views.SearchCourtView.as_view(), name='search_court'),
    path('add_court/', views.AddCourtView.as_view(), name='add_court'),
    path('delete_court/<int:pk>/', views.DeleteCourtView.as_view(), name='delete_court'),
    path('update_court/<int:pk>/', views.UpdateCourtView.as_view(), name='update_court'),
    path('court_detail/<int:pk>/', views.CourtDetailView.as_view(), name='court_detail'),
    path('court_list/', views.CourtListView.as_view(), name='court_list'),
    # ------------------------------------------------------------------------------------------#
    path('add_match/<int:pk>/', views.AddMatchView.as_view(), name='add_match'),
    # path('delete_match/<int:pk>/', views.DeleteMatchView.as_view(), name='delete_match'),
    # path('update_match/<int:pk>/', views.UpdateMatchView.as_view(), name='update_match'),
    path('matches_list/<int:pk>/', views.MatchesListView.as_view(), name='matches_list'),
]
