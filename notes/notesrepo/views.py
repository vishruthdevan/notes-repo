from django.db.models.fields import files
from django.http import response
from django.shortcuts import render, redirect
from django.views import generic
from django.views import View
from .models import *
from django.urls import reverse, reverse_lazy
from . import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login


def index(request):
    return render(request, 'notesrepo/index.html')

class Signup(View):
    def get(self, request):
        form = forms.RegisterForm()
        return render(request, "registration/signup.html", {'form' : form})

    def post(self, request):
        context = request.POST.copy()
        context['exp'] = '0'
        form = forms.RegisterForm(request.POST)
        aform = forms.AuthorForm(context)
        print(form.is_valid(), aform.is_valid())
        if form.is_valid() and aform.is_valid():
            user = form.save()
            user.refresh_from_db()
            aform = forms.AuthorForm(context, instance = user.author)
            aform.is_valid()
            aform.save()
            login(request, user)
            return redirect(reverse('index'))


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
        context["notes"] = Note.objects.filter(course__code = context['course'].code)
        return context
    
class CourseCreate(LoginRequiredMixin, View):
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


class NoteCreate(LoginRequiredMixin, generic.CreateView):
    model = Note
    fields = ['topic','note_file', 'author']
    template_name = 'notesrepo/note_create.html'

    def get_success_url(self) -> str:
        success_url = reverse_lazy('course_detail', kwargs = self.kwargs)
        return success_url
    
    def form_valid(self, form):
        print(self.request.user)
        data = form.save(commit=False)
        data.course = Course.objects.get(code = self.kwargs['code'])
        #data.author = Author.objects.get(owner = self.request.user)
        data.save()
        
        return super().form_valid(form)