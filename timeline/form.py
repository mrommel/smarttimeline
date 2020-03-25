from django import forms
from django.forms.widgets import TextInput

from .models import App, Version


class AppForm(forms.ModelForm):
    class Meta:
        model = App
        fields = '__all__'
        widgets = {
            'color': TextInput(attrs={'type': 'color'}),
        }


class VersionModelForm(forms.ModelForm):
    changelog = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Version
        fields = ['name', 'changelog', 'pub_date', ]
