from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View

from SwishApp.forms import SearchCourtForm
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



