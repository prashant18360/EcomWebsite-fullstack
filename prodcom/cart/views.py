from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from home.models import Productitem
from django.contrib.auth.models import User 
from cart.cart import *
from django.contrib import messages
#from .forms import CartAddProductForm



def cart_add(request):
    if request.method == 'POST':
        product_id = request.POST['product_id'] if 'product_id' in request.POST else ''
        loguser = request.user

        if loguser.is_anonymous:
            return HttpResponse("Something Went Wrong")

        customer = get_object_or_404(Account, user=loguser)

        productitem = get_object_or_404(Productitem, id=product_id)
        value = add(customer, productitem)

        if value == 0:
            messages.error(request, "Cannot added your last product add further in your cart because it is limited in quantity or Out of stock !!")

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
    


def cart_checkout(request):
    if request.method == 'POST':
        loguser = request.user
        
        if loguser.is_anonymous:
            return HttpResponse("Something Went Wrong")
        
        customer = get_object_or_404(Account, user=loguser)
        cart, totalcost = CartShow(customer)

        return render(request, 'cart/checkout.html', {'totalcost' : totalcost})

    else:
        return HttpResponse("404 - Not found")


def paymentcarddetails(request):
    if request.method == 'POST':
        loguser = request.user
        
        if loguser.is_anonymous:
            return HttpResponse("Something Went Wrong")
        
        customer = get_object_or_404(Account, user=loguser)
        cart, totalcost = CartShow(customer)

        otp = getPaymentOTP()
        numcode = getPaymentNumCode()

        Paymentotp.objects.create(customer=customer, otp=otp, numcode=numcode)
        sentpaymentotp(otp, totalcost, customer.user.email, customer.user.first_name)

        context = {'email' : customer.user.email, 'num' : numcode}

        return render(request, 'cart/paymentotp.html', context)

    else:
        return HttpResponse("404 - Not found")


def paymentotpverify(request):
    if request.method == 'POST':
        loguser = request.user

        code = request.POST['num'] if 'num' in request.POST else ''
        input_otp = request.POST['otp'] if 'otp' in request.POST else ''

        if loguser.is_anonymous or code == '' or input_otp == '':
            return HttpResponse("Something Went Wrong")

        
        customer = get_object_or_404(Account, user=loguser)
        #cart, totalcost = CartShow(customer)

        if input_otp.isdigit():
            inputotp = int(input_otp)

            otp_object = Paymentotp.objects.filter(customer=customer, numcode__exact=code).last()
            otp_objectexist = True if otp_object else False   
                
            if otp_objectexist:
                if not otp_object.IsExpired():
                    if inputotp == otp_object.otp:

                        
                        orderitemlist, ordertotalcost = OrderPlaced(customer)

                        if ordertotalcost == -1:
                            context = {'ordertotalcost' : 'not'}
                            messages.error(request, "Your Payment Cannot completed because one of the product is Out of Stock, Please Go back to cart and check")
                            return render(request, 'cart/Placedorder.html', context)
                        else:
                            context = {'orderitemlist' : orderitemlist, 'ordertotalcost' : ordertotalcost}
                            messages.success(request, "Your Payment Successfully Completed !! Your Order is Placed")
                            return render(request, 'cart/Placedorder.html', context)

                            
                    else:
                        context = {'email' : customer.user.email, 'num' : code}
                        messages.error(request, "You have entered the Wrong OTP !! Please Enter the correct otp ")
                        return render(request, 'cart/paymentotp.html', context)
                else:
                    context = {'email' : customer.user.email, 'num' : code}
                    messages.error(request, "Your entered OTP is being Expired !!")
                    return render(request, 'cart/paymentotp.html', context)
            else:
                return HttpResponse('403 - Something Went Wrong')
        else:
            context = {'email' : customer.user.email, 'num' : code}
            messages.error(request, "You have entered the Wrong OTP !! Please Enter the correct otp ")
            return render(request, 'cart/paymentotp.html', context)


    else:
        return HttpResponse("404 - Not found")



