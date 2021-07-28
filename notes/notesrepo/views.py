from django.http import response
from django.shortcuts import render
from django.views import generic
from django.views import View
from .models import Course

def index(request):
    return render(request, 'notesrepo/index.html')


# Create your views here.
class CourseListView(generic.ListView):
    model = Course
