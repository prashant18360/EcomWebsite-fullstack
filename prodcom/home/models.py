from django.db import models
from django.contrib.auth.models import User

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
    


