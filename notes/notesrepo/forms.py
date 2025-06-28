from django import forms
from django.forms import fields
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.contrib.auth.models import User

class CourseForm(forms.ModelForm):    
    class Meta:
        model = Course
        fields = '__all__'


class RegisterForm(UserCreationForm):
    name = forms.CharField(max_length=50)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('name',)

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'exp']