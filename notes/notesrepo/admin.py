from django.contrib import admin
from .models import Comment, Course, Note, Author
# Register your models here.

admin.site.register(Course)
admin.site.register(Note)
admin.site.register(Author)
admin.site.register(Comment)