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



def productpageData(productobj):
    dt = {}
    dt['id'] = productobj.id
    dt['name'] = productobj.name
    dt['description'] = productobj.description
    dt['category'] = productobj.category
    dt['stockquantity'] = productobj.quantity
    dt['price'] = productobj.price
    dt['image1'] = productobj.image1.url
    dt['image2'] = productobj.image2.url
    dt['seller'] = {'id' : productobj.seller.id, 'name' : productobj.seller.user.first_name + " " + productobj.seller.user.last_name}
    #print(dt)
    return dt
    
    
   



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


