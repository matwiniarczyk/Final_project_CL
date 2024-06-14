from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, UpdateView

from SwishApp.forms import SearchCourtForm, AddCourtForm
from SwishApp.models import Court, Sport, Match


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
            return redirect('court_detail', added_court.pk)
        return render(request, 'swishapp/add_court.html', {'form': form})


class DeleteCourtView(PermissionRequiredMixin, DeleteView):
    permission_required = ["swishapp.delete_court"]
    model = Court
    template_name = "swishapp/delete_court.html"
    success_url = reverse_lazy("court_list")


class UpdateCourtView(PermissionRequiredMixin, UpdateView):
    permission_required = ["swishapp.update_court"]
    model = Court
    form_class = AddCourtForm
    template_name = "swishapp/update_court.html"
    success_url = reverse_lazy("court_list")


class CourtDetailView(View):
    def get(self, request, pk):
        court = Court.objects.get(pk=pk)
        matches = Match.objects.filter(court=court)
        return render(request, 'swishapp/court_detail.html', {'court': court, 'matches': matches})


class CourtListView(View):
    def get(self, request):
        courts = Court.objects.all().order_by('location')
        return render(request, 'swishapp/court_list.html', {'courts': courts})


class AddMatchView(LoginRequiredMixin, View):
    def get(self, request, pk):
        court = Court.objects.get(pk=pk)
        day_choices = Match.DAY_CHOICES
        time_choices = Match.TIME_CHOICES
        sports = court.intended_for.all()
        return render(request, 'swishapp/add_match.html',
                      {'court': court,
                       'day_choices': day_choices,
                       'time_choices': time_choices,
                       'sports': sports
                       })

    def post(self, request, pk):
        court = Court.objects.get(pk=pk)
        day = request.POST['day']
        time = request.POST['time']
        sport_id = request.POST['sport']
        sport = Sport.objects.get(id=sport_id)
        added_by = request.user
        match = Match.objects.filter(court=court, day=day, time=time, sport=sport)
        if match.exists():
            messages.error(request, 'This match already exists')
            return redirect('add_match', pk=pk)
        else:
            added_match = Match.objects.create(sport=sport, day=day, time=time, added_by=added_by)
            added_match.court.set([court])
            messages.success(request, 'Match added')
            return redirect('court_detail', pk=court.pk)


class MatchesListView(View):
    def get(self, request, pk):
        court = Court.objects.get(pk=pk)
        matches = Match.objects.filter(court=court)
        return render(request, 'swishapp/court_detail.html', {'matches': matches,
                                                              'court': court})
