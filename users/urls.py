from django.http import request
from django.urls import path
from django.urls.conf import include
from . import views

urlpatterns = [
    path('signup/', views.Signup.as_view(), name='signup'),
]
