from django import forms

class FaceForm(forms.Form):
    img = forms.ImageField()
