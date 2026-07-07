from django import forms


class FaceForm(forms.Form):
    """Validate image input from either a file upload or a remote image URL."""

    img = forms.ImageField(required=False)
    image_url = forms.URLField(required=False)

    def clean(self):
        """Require at least one image source before starting analysis."""
        cleaned_data = super().clean()
        if not cleaned_data.get("img") and not cleaned_data.get("image_url"):
            raise forms.ValidationError("Upload an image or provide an image URL.")
        return cleaned_data