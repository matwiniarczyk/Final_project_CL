from django.urls import path
from Accounts import views


urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name="register"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
]