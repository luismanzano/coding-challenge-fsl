from django import forms

class CreateNewShortUrl(forms.Form):
    original_url = forms.CharField(label='original url')