from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.


class ToDo(models.Model):
    input_field = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.input_field