from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View


class CreateUserView(View):
    def get(self, request):
        return render(request, "accounts/create_user.html")

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_2 = request.POST.get('password2')
        if password != "" and password == password_2:
            u = User(username=username)
            u.set_password(password)
            u.save()
            return redirect('base')
        return render(request, "accounts/create_user.html",
                      {"error": "Passwords do not match, try again!"})


class LoginView(View):
    def get(self, request):
        return render(request, "accounts/login.html")

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            redirect_url = request.GET.get('next', 'base')
            login(request, user)
            return redirect(redirect_url)
        else:
            return redirect('login')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('base')
