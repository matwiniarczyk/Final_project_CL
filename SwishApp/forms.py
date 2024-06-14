from django import forms

from SwishApp.models import Court, Sport, Match


# WALIDATORY
def check_if_letters(value):
    if not value.isalpha():
        raise forms.ValidationError('Please enter letters only')


# ---------------------------------------------------------------------------------------------------------------------#

# FORMULARZE

class SearchCourtForm(forms.Form):
    location = forms.CharField(max_length=50, validators=[check_if_letters])
    intended_for = forms.ModelChoiceField(
        queryset=Sport.objects.all(),
        widget=forms.Select(),
    )


class AddCourtForm(forms.ModelForm):
    location = forms.CharField(max_length=50, validators=[check_if_letters])

    class Meta:
        model = Court
        fields = '__all__'


