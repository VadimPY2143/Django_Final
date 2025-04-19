from django.db import models
from django.contrib.auth.models import AbstractUser


class CreateUser(AbstractUser):
    phone_number = models.CharField(max_length=15, null=True)
    avatar = models.ImageField(null=True, blank=True)



