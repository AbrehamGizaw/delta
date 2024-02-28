from django import forms
from tinymce.widgets import TinyMCE
from .models import *


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ("title", "name", "phone", "email", "image", "original_document", "cv_document", "supplementary_document", "letter")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Write your title"}),
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Write your name"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Write your phone"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Write your email"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "original_document": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "cv_document": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "supplementary_document": forms.ClearableFileInput(attrs={"class": "form-control"}),
            'letter': TinyMCE(attrs={'cols': 20, 'rows': 20}),
        }

class CallApplicationForm(forms.ModelForm):
    class Meta:
        model = CallApplication
        fields = ("title", "phone","email", "start_date", "end_date", "assistant_name", "document")
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Write your email"}),
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Write your title here"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Write your phone"}),
            "start_date": forms.DateTimeInput(attrs={"class": "form-control"}),
            "end_date": forms.DateInput(attrs={"class": "form-control"}),
            "assistant_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Write assistant name"}),
            "document": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

class EventsForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = ("title", "image", "event_handler", "place", "start_date", "end_date", "category")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Write your title"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "event_handler": forms.TextInput(attrs={"class": "form-control", "placeholder": "Write name of event handler"}),
            "place": forms.TextInput(attrs={"class": "form-control", "placeholder": "Write name of the place"}),
            "start_date": forms.DateInput(attrs={"class": "form-control"}),
            "end_date": forms.DateInput(attrs={"class": "form-control"}),
            'category': forms.Select(attrs={'type':'dropdown', 'class':'custom-select ', }),
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ("name", "email", "phone", "interest", "message")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Write your name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Write your email"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Write your phone"}),
            "interest": forms.TextInput(attrs={"class": "form-control", "placeholder": "Write your interest"}),
            'message': forms.Textarea(attrs={'class':'field-control', 'placeholder':' Write your content here ...', 'required':'false'}),
            }



class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery 
        fields = ('title', 'category')
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control', 'placeholder':' Title'}),
            'category': forms.Select(attrs={'type':'dropdown', 'class':'custom-select ', }),
        }

class Galley_ImageForm(forms.ModelForm):
    image = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control'})
    )

    class Meta:
        model = Gallery_Image
        fields = ('image',)




        
class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ("title", "image", "category", "description")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Write your title"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "custom-select"}),
            "description": TinyMCE(attrs={'cols': 20, 'rows': 20}),
        }

class ResearchForm(forms.ModelForm):
    class Meta:
        model = Research
        fields = ("title", "author", "keywords", "document", "approved")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Write your title here"}),
            "author": forms.TextInput(attrs={"class": "form-control", "placeholder": "Write name of author here"}),
            "keywords": forms.TextInput(attrs={"class": "form-control", "placeholder": "Write your keywords here"}),
            "document": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "approved": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "abstract": TinyMCE(attrs={"class": "field-control", "placeholder": "Write your concept here ...", "required": "false"})
        }

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ("name", "image", "role", "wing", "phone", "email", "is_active")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": " Name"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "role": forms.TextInput(attrs={"class": "form-control", "placeholder": " role"}),
            "wing": forms.Select(attrs={"class": "custom-select"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": " phone"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": " email"}),
            "is_active": forms.CheckboxInput(attrs={"class": "switchery", "type": "checkbox"}),
        }