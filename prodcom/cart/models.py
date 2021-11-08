from django.db import models
from home.models import *

# Create your models here.

class shopcart(models.Model):
    customer = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Productitem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    datetime = models.DateTimeField(auto_now=True)


class placedorder(models.Model):
    customer = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Productitem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    datetime = models.DateTimeField(auto_now=True)

