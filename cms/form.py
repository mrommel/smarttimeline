from django import forms

from cms.models import Paragraph


class ParagraphModelForm(forms.ModelForm):
    headline = forms.CharField(
        label='Headline',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Paragraph
        fields = ['headline', 'text', 'css', ]