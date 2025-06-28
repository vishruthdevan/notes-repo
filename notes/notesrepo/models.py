from django.db import models

# Create your models here.
class Note(models.Model):
    topic = models.CharField(max_length=50)
    note_file = models.FileField(upload_to='notes/%Y/%m/%d/')
    course = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)

class Course(models.Model):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

class Author(models.Model):
    name = models.CharField(max_length=50)
    exp = models.IntegerField()