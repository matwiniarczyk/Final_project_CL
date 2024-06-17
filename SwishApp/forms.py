from django import forms

from SwishApp.models import Court, Sport, Match, Comment


# WALIDATORY
def check_if_letters(value):
    if not value.replace(' ', '').isalpha():
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


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control'})
        }
