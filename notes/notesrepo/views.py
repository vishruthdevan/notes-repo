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

# class NoteCreate(View):
#     template_name = 'notesrepo/note_create.html'
#     success_url = reverse_lazy('course_list')

#     def get(self, request, *args, **kwargs):
#         form = forms.NoteForm()
#         ctx = {'form': form}
#         return render(request, self.template_name, ctx)

#     def post(self, request, *args, **kwargs):
#         form = forms.NoteForm(request.POST, request.FILES or None)

#         if not form.is_valid():
#             ctx = {'form': form}
#             return render(request, self.template_name, ctx)

#         # Add owner to the model before saving
#         form.save(commit=True)
#         return redirect(self.success_url)


class NoteCreate(generic.CreateView):
    model = Note
    fields = '__all__'
    template_name = 'notesrepo/note_create.html'

    def get_success_url(self) -> str:
        success_url = reverse_lazy('course_detail', kwargs = self.kwargs)
        return success_url