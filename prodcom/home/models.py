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
