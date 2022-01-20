from django.views.decorators.csrf import csrf_exempt
from django.db.utils import IntegrityError
from django.utils.decorators import method_decorator
from django.db.models.fields import files
from django.http import request, response
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.views import View
from .models import *
from django.urls import reverse, reverse_lazy
from . import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator


def index(request):
    return render(request, 'notes/index.html')


class CourseListView(LoginRequiredMixin, generic.ListView):
    model = Course


class CourseDetailView(LoginRequiredMixin, generic.DetailView):
    model = Course
    slug_url_kwarg = 'code'
    slug_field = 'code'
    query_pk_and_slug = True
    code = ''

    def get_context_data(self, **kwargs):
        search = self.request.GET.get("search", False)
        context = super().get_context_data(**kwargs)

        if search:
            q = Note.objects.filter(course__code=context['course'].code)
            q = q.filter(topic__contains=search)
        else:
            q = Note.objects.filter(course__code=context['course'].code)

        page = Paginator(q.order_by('id'), 10)
        context["notes"] = page.get_page(self.request.GET.get("page", 1))
        context["comments"] = Comment.objects.all()
        comment_form = forms.CommentForm()
        context["comment_form"] = comment_form
        author = Author.objects.get(user=self.request.user)
        liked = author.liked.all()
        context["liked"] = liked
        return context


class CourseCreate(LoginRequiredMixin, View):
    model = Course
    success_url = reverse_lazy('course_list')
    template_name = 'notes/course_create.html'

    def get(self, request):
        form = forms.CourseForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = forms.CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        context = {'form': form}
        return render(request, self.template_name, context)


class NoteCreate(LoginRequiredMixin, generic.CreateView):
    model = Note
    fields = ['topic', 'note_file']
    template_name = 'notes/note_create.html'

    def get_success_url(self):
        print("this")
        success_url = reverse_lazy('course_detail', kwargs=self.kwargs)
        return success_url

    def form_valid(self, form):
        data = form.save(commit=False)
        data.course = Course.objects.get(code=self.kwargs['code'])
        author = Author.objects.get(user=self.request.user)
        author.exp += 10
        author.save()
        data.author = author
        data.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class NoteDelete(LoginRequiredMixin, generic.DeleteView):
    model = Note

    def get_success_url(self) -> str:
        success_url = reverse_lazy('course_detail', kwargs={
                                   'code': self.kwargs['code']})
        return success_url

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(author__user=self.request.user)

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        author = Author.objects.get(user=self.request.user)
        if author.exp - 10 < 0:
            author.exp = 0
        else:
            author.exp -= 10
        author.save()
        return HttpResponseRedirect(success_url)


class NoteUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Note
    fields = ['topic', 'note_file']
    template_name = 'notes/note_create.html'

    def get_success_url(self):
        success_url = reverse_lazy('course_detail', kwargs={
                                   'code': self.kwargs['code']})
        return success_url

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(author__user=self.request.user)


class CommentCreate(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        author = Author.objects.get(user=self.request.user)
        author.exp += 5
        author.save()
        c = Comment(text=request.POST['text'], note=Note.objects.get(
            id=kwargs['pk']), author=author)
        c.save()
        return redirect(reverse('course_detail', kwargs={"code": self.kwargs['code']}))


class CommentDelete(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        c = get_object_or_404(Comment, id=kwargs['cid'])
        author = c.author
        if author.exp - 5 < 0:
            author.exp = 0
        else:
            author.exp -= 5
        author.save()
        c.delete()
        return redirect(reverse('course_detail', kwargs={"code": self.kwargs['code']}))


@method_decorator(csrf_exempt, name='dispatch')
class NoteLike(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        note = get_object_or_404(Note, id=kwargs['pk'])
        author = get_object_or_404(Author, user=request.user)
        note.like.add(author)
        note.save()
        return redirect(reverse('course_detail', kwargs={'code': kwargs['code']}))


@method_decorator(csrf_exempt, name='dispatch')
class NoteDislike(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        note = get_object_or_404(Note, id=kwargs['pk'])
        author = get_object_or_404(Author, user=request.user)
        note.like.remove(author)
        note.save()
        return redirect(reverse('course_detail', kwargs={'code': kwargs['code']}))
