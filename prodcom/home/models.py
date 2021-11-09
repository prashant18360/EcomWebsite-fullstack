from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

# Create your models here.
class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=15, default="buyer") #buyer/seller
    address = models.CharField(max_length=100)
    contactnum = models.CharField(max_length=15)

class ApplyForSeller(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default="pending") #pending/approved/rejected
    document = models.FileField(upload_to='documents/')


class Emailotp(models.Model):
    username = models.CharField(max_length=50)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    passw = models.CharField(max_length=50)
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



# Create your models here.
class Productitem(models.Model):
    seller = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    category = models.CharField(max_length=50)
    quantity = models.IntegerField()
    price = models.FloatField()
    image1 = models.ImageField(upload_to='productitem/%m/%d/')
    image2 = models.ImageField(upload_to='productitem/%m/%d/')
    


