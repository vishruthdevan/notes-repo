from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from users.models import Author
# Create your models here.


class Note(models.Model):
    topic = models.CharField(max_length=50)
    note_file = models.FileField(upload_to='notes/%Y/%m/%d/')
    course = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey('users.Author', on_delete=models.CASCADE)
    comments = models.ManyToManyField(
        Author, through='Comment', related_name='author_comments')
    like = models.ManyToManyField(Author, related_name='liked')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.topic)


class Course(models.Model):
    code = models.SlugField(max_length=50)
    name = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.code) + ' - ' + str(self.name)


class Comment(models.Model):
    text = models.CharField(max_length=200)
    author = models.ForeignKey('users.Author', on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if len(self.text) < 15:
            return self.text
        return self.text[:11] + ' ...'
