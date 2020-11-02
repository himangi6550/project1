from django.db import models
from django.conf import settings

# Create your models here.
status_choices=[
    ("PENDING","PENDING"),
    ("BOUGHT","BOUGHT"),
    ("NOT AVAILABLE","NOT AVAILABLE") ]

class Item(models.Model):

    itemname = models.CharField(max_length=100)
    itemquantity = models.CharField(max_length=100)
    itemstatus = models.CharField(max_length=20,choices=status_choices)
    date = models.DateField()

    def __str__(self):
        return self.itemname
