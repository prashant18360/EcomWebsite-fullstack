from decimal import Decimal
from django.conf import settings
from home.models import *
from cart.models import *
import re
import random
import string
from django.core.mail import send_mail
from django.conf import settings


def add(customer, product):
    cartitem = shopcart.objects.filter(customer=customer, product=product).first()
    if cartitem:
        if product.quantity - cartitem.quantity - 1 >= 0:
            cartitem.quantity = cartitem.quantity + 1
            cartitem.save()
            return 1
        else:
            return 0
    else:
        if product.quantity - 1 >= 0:
            shopcart.objects.create(customer=customer, product=product, quantity=1)
            return 1
        else:
            return 0

def remove(customer, product):
    
    cartitem = shopcart.objects.filter(customer=customer, product=product).first()
    if cartitem:
        if cartitem.quantity - 1 > 0:
            cartitem.quantity = cartitem.quantity - 1
            cartitem.save()
        else:
            cartitem.delete()
  
    else:
        return HttpResponse("Something Went Wrong")


def CartShow(customer):
    cart = shopcart.objects.filter(customer=customer)
    cartitemlist = []
    carttotalcost = 0
    if cart:
        for cartitem in cart:
            dt = {}
            dt['productid'] = cartitem.product.id
            dt['productname'] = cartitem.product.name
            dt['productimage'] = cartitem.product.image1.url
            dt['quantity'] = cartitem.quantity
            dt['productcost'] = cartitem.product.price
            dt['producttotalcost'] = cartitem.quantity*(cartitem.product.price)
            
            carttotalcost += dt['producttotalcost']
            cartitemlist.append(dt)
    
    return cartitemlist, carttotalcost




def getPaymentOTP():
    return(random.randint(10000000, 99999999))

def getPaymentNumCode():
    code = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 8))
    while Paymentotp.objects.filter(numcode__exact=code).exists():
        code = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 8))
    return code



def sentpaymentotp(otp, amount, email, fname):
    OTPmessage = f"Hi {fname},\n Your 8 digit OTP is {otp} for payment ₹ {amount} .\n This OTP is valid for only 10 Minutes.  \n\n Thanks"
                
    send_mail("FCSproject Payment OTP", 
            OTPmessage, 
            settings.EMAIL_HOST_USER, 
            [email], 
            fail_silently = False)




def OrderPlaced(customer):
    cart = shopcart.objects.filter(customer=customer)
    
    orderitemlist = []
    ordertotalcost = 0
    
    if cart:
        for cartitem in cart:
            placedorder.objects.create(customer=customer, product=cartitem.product, quantity=cartitem.quantity)
            
            if CheckproductQuantity(cartitem.product.id, cartitem.quantity):
                
                dt = {}
                dt['productname'] = cartitem.product.name
                dt['productimage'] = cartitem.product.image1.url
                dt['quantity'] = cartitem.quantity
                dt['productcost'] = cartitem.product.price
                dt['producttotalcost'] = cartitem.quantity*(cartitem.product.price)
            
                ordertotalcost += dt['producttotalcost']
                orderitemlist.append(dt)

            else:
                return [], -1
        
        shopcart.objects.filter(customer=customer).delete()

    return orderitemlist, ordertotalcost
    


def CheckproductQuantity(productid, qty):
    productitemobj = Productitem.objects.filter(id=productid).first()

    if productitemobj.quantity - qty >= 0:
        productitemobj.quantity = productitemobj.quantity - qty
        productitemobj.save()
        return True
    else:
        return False



'''
class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, productitem, quantity=1, update_quantity=False):
        #print(productitem)
        product_id = str(productitem.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(productitem.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, productitem):
        product_id = str(productitem.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Productitem.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True



'''

