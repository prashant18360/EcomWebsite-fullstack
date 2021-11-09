from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from cart import views


app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/', views.cart_add, name='cart_add'),
    path('remove/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.cart_checkout, name='cart_checkout'), 
    path('payment/carddetails/', views.paymentcarddetails, name='paymentcarddetails'),
    path('payment/otpverify/', views.paymentotpverify, name='paymentotpverify'),

]

