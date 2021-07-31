from django.http import request
from django.urls import path
from django.urls.conf import include
from . import views

#app_name = 'notesrepo'
urlpatterns = [
    path('', views.index),
    path('courses/', views.CourseListView.as_view(), name = 'course_list'),
    path('courses/create/', views.CourseCreate.as_view(), name = 'course_create'),
    path('courses/<slug:code>/', views.CourseDetailView.as_view(), name = 'course_detail'),
    path('courses/<slug:code>/upload-note/', views.NoteCreate.as_view(), name = 'note_create'),
    # path('courses/<slug:code>',),
    # path('courses/<slug:code>/notes',),
]