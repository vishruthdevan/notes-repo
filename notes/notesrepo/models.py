from django.db import models
from django.conf import settings
# Create your models here.
class Note(models.Model):
    topic = models.CharField(max_length=50)
    note_file = models.FileField(upload_to='notes/%Y/%m/%d/')
    course = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.topic)

class Course(models.Model):
    code = models.SlugField(max_length=50)
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.code) + ' - ' + str(self.name)

class Author(models.Model):
    name = models.CharField(max_length=50)
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    exp = models.IntegerField()

    def __str__(self):
        return self.name
