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
        fields = ['pub_date', 'name', 'changelog', ]


class AllRatingsForm(forms.Form):
    date = forms.DateField(
        label='date published',
        widget=forms.DateInput(
            attrs={'class': 'form-control'}
        ))
    myf_android = forms.DecimalField(
        max_digits=3,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={'class': 'form-control'}
        )
    )
    myf_ios = forms.DecimalField(
        max_digits=3,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={'class': 'form-control'}
        )
    )
