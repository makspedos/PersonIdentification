from django import forms

class FaceForm(forms.Form):
    img = forms.ImageField(required=False)
    url = forms.URLField(required=False)