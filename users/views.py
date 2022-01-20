from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views import View
from .models import *
from django.urls import reverse
from . import forms
from django.contrib.auth import login
from django.contrib.auth.models import User


class Signup(View):
    def get(self, request):
        form = forms.RegisterForm()
        return render(request, "registration/signup.html", {'form': form})

    def post(self, request):
        context = request.POST.copy()
        context['exp'] = 0
        form = forms.RegisterForm(request.POST)
        aform = forms.AuthorForm(context)
        if form.is_valid() and aform.is_valid():
            form.save()
            user = User.objects.get(username=request.POST['username'])
            instance = aform.save(commit=False)
            instance.user = user
            instance.save()
            login(self.request, user)
            return redirect(reverse('index'))
        else:
            return render(self.request, 'registration/signup.html', {'form': form})
