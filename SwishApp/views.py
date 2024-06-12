from django.shortcuts import render, redirect
from django.views import View

from SwishApp.forms import SearchCourtForm, AddCourtForm
from SwishApp.models import Court, Sport


class SearchCourtView(View):
    def get(self, request):
        form = SearchCourtForm()
        return render(request, "swishapp/search_court.html", {"form": form})

    def post(self, request):
        form = SearchCourtForm(request.POST)
        if form.is_valid():
            location = form.cleaned_data['location']
            intended_for = form.cleaned_data['intended_for']
            searched_courts = Court.objects.filter(
                location__icontains=location,
                intended_for=intended_for
            )
            if searched_courts.exists():
                return render(request, 'swishapp/filtered_court_list.html',
                              {'searched_courts': searched_courts})
            else:
                return render(request, 'swishapp/no_matching_courts.html')
        else:
            return render(request, "swishapp/search_court.html", {"form": form})


class AddCourtView(View):
    def get(self, request):
        form = AddCourtForm()
        return render(request, 'swishapp/add_court.html', {'form': form})

    def post(self, request):
        form = AddCourtForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            location = form.cleaned_data['location']
            intended_for = form.cleaned_data['intended_for']
            free_parking_around = form.cleaned_data['free_parking_around']
            added_court = Court.objects.create(
                name=name,
                location=location,
                free_parking_around=free_parking_around)
            added_court.intended_for.set(intended_for)
            return redirect('court_list')
        return render(request, 'swishapp/add_court.html', {'form': form})


class CourtListView(View):
    def get(self, request):
        courts = Court.objects.all()
        return render(request, 'swishapp/court_list.html', {'courts': courts})
