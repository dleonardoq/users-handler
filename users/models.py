from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils import timezone


class Users(AbstractBaseUser):
    document_type = models.CharField(max_length=5)
    document_number = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
