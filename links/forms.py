from django import forms
from .models import Link


class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ['author', 'title', 'date_published', 'url']

        widgets = {
            'author': forms.TextInput(attrs={'class': 'form-control bg-white border-md'}),
            'title': forms.TextInput(attrs={'class': 'form-control bg-white border-md'}),
            'date_published': forms.DateInput(attrs={'class': 'form-control bg-white border-md'}),
            'url': forms.URLInput(attrs={'class': 'form-control bg-white border-md'}),
        }


