
from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    
    path('', views.home, name='home'),
    path('signup', views.signupprocess, name='signup'),
    path('login', views.loginprocess, name='login'),
    path('logout', views.logoutprocess, name='logout'),

    path('applyforseller', views.applyforseller, name='applyforseller'),
    path('sellerapprove', views.sellerapprove, name='sellerapprove'),
    path('sellerreject', views.sellerreject, name='sellerreject'),

    path('<str:username>', views.profile, name="profile"),

]
