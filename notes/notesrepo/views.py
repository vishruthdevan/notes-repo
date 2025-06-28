from django.db.models.fields import files
from django.http import response
from django.shortcuts import render, redirect
from django.views import generic
from django.views import View
from .models import *
from django.urls import reverse, reverse_lazy
from . import forms


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
    
class CourseCreate(View):
    model = Course
    success_url = reverse_lazy('course_list')
    template_name = 'notesrepo/course_create.html'
    
    def get(self, request):
        form = forms.CourseForm()
        context = {'form' : form}
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = forms.CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        context = {'form':form}
        return render(request, self.template_name, context)


class NoteCreate(generic.CreateView):
    model = Note
    fields = '__all__'
    template_name = 'notesrepo/note_create.html'
    success_url = reverse_lazy('course_list')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)