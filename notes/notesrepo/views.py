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
from django.contrib.auth.models import User

def index(request):
    return render(request, 'notesrepo/index.html')

class Signup(View):
    def get(self, request):
        form = forms.RegisterForm()
        return render(request, "registration/signup.html", {'form' : form})

    def post(self, request):
        context = request.POST.copy()
        context['exp'] = 0
        form = forms.RegisterForm(request.POST)
        aform = forms.AuthorForm(context)
        if form.is_valid() and aform.is_valid():
            form.save()
            print(User.objects.get(username = request.POST['username']))
            user = User.objects.get(username = request.POST['username'])
            instance = aform.save(commit=False)
            instance.user = user
            instance.save()
            login(self.request, user)
            return redirect(reverse('index'))
        else:
            return render(self.request, 'registration/signup.html', {'form' : form})


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
    fields = ['topic','note_file']
    template_name = 'notesrepo/note_create.html'

    def get_success_url(self) -> str:
        success_url = reverse_lazy('course_detail', kwargs = self.kwargs)
        return success_url
    
    def form_valid(self, form):
        print(self.request.user)
        data = form.save(commit=False)
        data.course = Course.objects.get(code = self.kwargs['code'])
        author = Author.objects.get(user = self.request.user)
        author.exp += 10
        author.save()
        data.author = author
        data.save()
        return super().form_valid(form)

class NoteDelete(LoginRequiredMixin, generic.DeleteView):
    model = Note
    
    def get_success_url(self) -> str:
        success_url = reverse_lazy('course_detail', kwargs = {'code' : self.kwargs['code']})
        return success_url

    def get_queryset(self):
        qs = super().get_queryset()
        print(qs)
        return qs.filter(author__user=self.request.user)
        
class NoteUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Note
    fields = ['topic', 'note_file']
    template_name = 'notesrepo/note_create.html'

    def get_success_url(self):
        success_url = reverse_lazy('course_detail', kwargs =  {'code' : self.kwargs['code']})
        return success_url
    
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(author__user = self.request.user)