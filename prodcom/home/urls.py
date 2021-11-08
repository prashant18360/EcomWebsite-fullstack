
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

    path('addproduct', views.addproduct, name='addproduct'), 

    path('seller/catalog', views.sellercatalog, name='sellercatalog'),
    path('seller/productedit/page', views.sellereditproductpage, name='sellereditproductpage'), 
    path('seller/product/edit', views.sellereditproduct, name='sellereditproduct'), 
    path('seller/product/remove', views.sellerremoveproduct, name='sellerremoveproduct'),

    path('product/<str:id>/<str:name>', views.product, name='product'),

    path('<str:username>', views.profile, name="profile"),
    path('<str:username>/allapplication', views.allapplication, name="allapplication"),
    path('<str:username>/allseller', views.allseller, name="allseller"),
    path('<str:username>/allbuyer', views.allbuyer, name="allbuyer"),
    path('<str:username>/allproduct', views.allproduct, name="allproduct"),

    path('<str:username>/seller/remove', views.sellerremove, name="sellerremove"),
    path('<str:username>/buyer/remove', views.buyerremove, name="buyerremove"),
    path('<str:username>/product/remove', views.productremove, name="productremove"),
    

]
