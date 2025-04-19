from django.db import models
from base import TimeStamp


class CreateObject(TimeStamp):
    OBJECT_CHOICES = [
        ('HOTEL', 'hotel'),
        ('APARTMENTS', 'apartments'),
        ('HOUSE', 'house'),
        ('VILLA', 'villa'),
        ('MOTEL', 'motel')
    ]
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(blank=True, null=True)
    settlement_type = models.CharField(max_length=10, choices=OBJECT_CHOICES, default='HOTEL', null=False)
    price = models.PositiveIntegerField(null=False)
    image = models.CharField(max_length=255, null=False)



