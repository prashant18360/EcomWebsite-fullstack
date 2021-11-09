from home.models import *
import re
import random
import string
from django.core.mail import send_mail
from django.conf import settings


def generateOTP():
    return(random.randint(100000, 999999))


def generateNumCode():
    code = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 8))
    while Emailotp.objects.filter(numcode__exact=code).exists():
        code = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 8))
    return code


def sendOTPEmail(otp, email):
        
    OTPmessage = f"Hello new User,\n Your 6 digit OTP for Email Varification is {otp}\n This OTP is valid for only 10 Minutes.  \n\n Thanks"
                
    send_mail("FCSproject Account Email verification", 
            OTPmessage, 
            settings.EMAIL_HOST_USER, 
            [email], 
            fail_silently = False)


