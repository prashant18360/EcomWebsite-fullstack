
from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    
    path('', views.home, name='home'),
    path('signup', views.signupprocess, name='signup'),
    path('login', views.loginprocess, name='login'),
    path('logout', views.logoutprocess, name='logout'),
]
