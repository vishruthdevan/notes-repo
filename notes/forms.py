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


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text': 'Add a comment'
        }
