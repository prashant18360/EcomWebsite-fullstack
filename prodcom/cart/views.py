from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from home.models import Productitem
from cart.cart import *
#from .forms import CartAddProductForm



def cart_add(request):
    if request.method == 'POST':
        product_id = request.POST['product_id'] if 'product_id' in request.POST else ''
        loguser = request.user

        if loguser.is_anonymous:
            return HttpResponse("Something Went Wrong")

        customer = get_object_or_404(Account, user=loguser)

        productitem = get_object_or_404(Productitem, id=product_id)
        add(customer, productitem)

        return redirect('cart:cart_detail')
    else:
        return HttpResponse("404 - Not found")


def cart_remove(request):

    if request.method == 'POST':
        product_id = request.POST['product_id'] if 'product_id' in request.POST else ''
        loguser = request.user

        if loguser.is_anonymous:
            return HttpResponse("Something Went Wrong")

        customer = get_object_or_404(Account, user=loguser)

        productitem = get_object_or_404(Productitem, id=product_id)
        remove(customer, productitem)

        return redirect('cart:cart_detail')
    else:
        return HttpResponse("404 - Not found")


    


def cart_detail(request):
    product_id = request.POST['product_id'] if 'product_id' in request.POST else ''
    loguser = request.user

    if loguser.is_anonymous:
            return HttpResponse("Something Went Wrong")

    customer = get_object_or_404(Account, user=loguser)

    cart, totalcost = CartShow(customer)

    return render(request, 'cart/detail.html', {'cart': cart, 'totalcost' : totalcost})
    


    #cart = Cart(request)
    #for item in cart:
    #    item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    #return render(request, 'cart/detail.html', {'cart': cart})
