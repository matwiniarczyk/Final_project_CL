from django import forms

from SwishApp.models import Court, Sport


class SearchCourtForm(forms.Form):
    location = forms.CharField(max_length=50)
    intended_for = forms.ModelChoiceField(
        queryset=Sport.objects.all(),
        widget=forms.Select(),
    )
