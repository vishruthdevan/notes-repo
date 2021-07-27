from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('courses/',),
    path('courses/<slug:code>',),
    path('courses/<slug:code>/notes',),
]