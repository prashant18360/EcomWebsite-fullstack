from django.db import models
from home.models import *
from django.utils import timezone
import datetime

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


class Paymentotp(models.Model):
    customer = models.ForeignKey(Account, on_delete=models.CASCADE)
    numcode = models.CharField(max_length=10)
    time_stp = models.DateTimeField(default=timezone.now)
    otp = models.IntegerField()

    #this function return if an OTP is expired
    def IsExpired(self):
        time = self.time_stp + datetime.timedelta(minutes=10)
        if time.replace(tzinfo=None) < timezone.now().replace(tzinfo=None):
            return True
        else:
            return False


