from django import forms
from django.forms import fields
from .models import *

class CourseForm(forms.ModelForm):
    
    class Meta:
        model = Course
        fields = '__all__'
