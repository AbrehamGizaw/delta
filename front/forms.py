from django import forms
from .models import *


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = [
            "title",
            "image",
            "description",
            "category",
            "post_date",
            "post_by",
        ]
        widgets = {
            "post_date": forms.DateInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "category": forms.Select(
                attrs={"type": "dropdown", "class": "form-control"}
            ),
            "post_by": forms.Select(
                attrs={"type": "dropdown", "class": "form-control"}
            ),
        }





class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ["category", "image", "title", "post_date", "post_by"]
        widgets = {
            "category": forms.Select(
                attrs={"type": "dropdown", "class": "form-control"}
            ),
            "post_by": forms.Select(
                attrs={"type": "dropdown", "class": "form-control"}
            ),
        }


class GalleyImageForm(forms.ModelForm):

    image = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                "multiple": True,
            }
        ),
    )

    class Meta:
        model = GalleryImage
        fields = ("image",)







