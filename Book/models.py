from django.db import models
from django.core.validators import MinValueValidator
from Auth.models import CreateUser
from Object.models import CreateObject
from base import TimeStamp


class Booking(TimeStamp):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    email = models.EmailField()
    human_count = models.IntegerField(validators=[MinValueValidator(1)])
    date_from = models.DateField(null=False)
    date_to = models.DateField(null=False)
    object = models.ForeignKey(CreateObject, on_delete=models.CASCADE)
    user = models.ForeignKey(CreateUser, on_delete=models.CASCADE, null=True, blank=True)
    paid = models.BooleanField(default=False)

