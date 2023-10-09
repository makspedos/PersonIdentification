from django import forms

class FaceForm(forms.Form):
    image =forms.ImageField(required=True, label='img')