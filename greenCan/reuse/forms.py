from django import forms
from .models import Post

class FormPost(forms.ModelForm):
    class Meta:
        model= Post
        fields= ["id", "title", "category", "phone_number", "email", "zip_code", "description", "user", "approved", "still_available"]
