from django import forms

class FaceForm(forms.Form):
    img = forms.ImageField(required=False)
    url = forms.URLField(required=False)

    # def clean(self):
    #     cleaned_data = super().clean()
    #     img = cleaned_data.get('img')
    #     url = cleaned_data.get('image_url')
    #
    #     # Check if both fields are empty
    #     if not img and not url:
    #         raise forms.ValidationError("Завантажте зображення або введіть url.")
    #
    #     return cleaned_data