import re
#from django.contrib.auth.models import User
from home.models import *


def validatepassword(password):
    if len(password) < 8:
        return False
    elif not re.search("[a-z]", password):
        return False
    elif not re.search("[A-Z]", password):
        return False
    elif not re.search("[0-9]", password):
        return False
    elif not re.search("[~`^<>:;?*#@$!%&._+-=]", password):
        return False
    elif re.search("/s", password):
        return False
    return True


def validateusername(username):
    if len(username) > 20:
        return False
    for usr in username:
        if usr.isalnum():
            pass
        else:   
            return False
    else:
        return True


def profilepageData(accountobj):
    context = {'username' : accountobj.user.username}
    context['fullname'] = accountobj.user.first_name + " " + accountobj.user.last_name
    context['email'] = accountobj.user.email
    context['contact'] = accountobj.contactnum
    context['address'] = accountobj.address
    context['role'] = accountobj.role

    return context


def AdminConsoleApplication(): 
    application = ApplyForSeller.objects.filter(status="pending")

    return {"application" : application}



def AdminConsoleSeller(): 
    sellerlist = Account.objects.filter(role='seller')

    return {"sellerlist" : sellerlist}


def AdminConsoleBuyer(): 
    buyerlist = Account.objects.filter(role='buyer')

    return {"buyerlist" : buyerlist}



def AdminConsoleProduct(): 
    productlist = Productitem.objects.all()

    return {"productlist" : productlist}


