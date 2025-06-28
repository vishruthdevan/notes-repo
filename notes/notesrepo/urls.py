from django.http import request
from django.urls import path
from django.urls.conf import include
from . import views


urlpatterns = [
    path('', views.index),
    path('courses/', views.CourseListView.as_view()),
    # path('courses/<slug:code>',),
    # path('courses/<slug:code>/notes',),
]