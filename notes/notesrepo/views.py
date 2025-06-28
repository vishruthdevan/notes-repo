from django.http import response
from django.shortcuts import render
from django.views import generic
from django.views import View
from .models import *

def index(request):
    return render(request, 'notesrepo/index.html')


# Create your views here.
class CourseListView(generic.ListView):
    model = Course

class CourseDetailView(generic.DetailView):
    model = Course
    slug_url_kwarg = 'code'
    slug_field = 'code'
    query_pk_and_slug = True
    code = ''
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        context["notes"] = Note.objects.filter(course__code = context['course'].code)
        return context
    