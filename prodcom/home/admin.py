from django.contrib import admin
from home.models import *

# Register your models here.
admin.site.register((Account, ApplyForSeller, Productitem))
admin.site.register(Emailotp)

