from django.urls import path

from SwishApp import views

urlpatterns = [
    path('search_court/', views.SearchCourtView.as_view(), name='search_court'),
    path('add_court/', views.AddCourtView.as_view(), name='add_court'),
]
