from django.db import models
from django.forms import CharField

# Create your models here.

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=256, default=None)
    first_name = models.CharField(max_length=100, default=None)
    regNo = models.CharField(max_length=100, default=None)
    gender = models.CharField(max_length=100, default=None)
    email = models.CharField(max_length=100, default=None)
	

    def __str__(self):
        return self.regNo
