from decimal import Decimal
from django.conf import settings
from home.models import *
from cart.models import *


def add(customer, product):
    cartitem = shopcart.objects.filter(customer=customer, product=product).first()
    if cartitem:
        cartitem.quantity = cartitem.quantity + 1
        cartitem.save()
    else:
        shopcart.objects.create(customer=customer, product=product, quantity=1)

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

