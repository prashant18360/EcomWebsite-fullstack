from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User 
from django.contrib.auth  import authenticate,  login, logout
from django.contrib import messages
from home.utility import *
from home.helper import *
from home.models import *

# Create your views here.
def home(request):
    productlist = []
    for obj in Productitem.objects.all()[:10]:
        dt = {}
        dt['id'] = obj.id
        dt['name'] = obj.name
        dt['description'] = obj.description
        dt['quantity'] = obj.quantity
        dt['price'] = obj.price
        dt['image2'] = obj.image2.url
        dt['image1'] = obj.image1.url
        productlist.append(dt)
    
    return render(request, 'home/home.html', {'productlist' : productlist})


def signupprocess(request):
    if request.method=="POST":
        
        username=request.POST['username'] if 'username' in request.POST else ''
        email=request.POST['email'] if 'email' in request.POST else ''
        fname=request.POST['fname'] if 'fname' in request.POST else ''
        lname=request.POST['lname'] if 'lname' in request.POST else ''
        pass1=request.POST['pass1'] if 'pass1' in request.POST else ''
        pass2=request.POST['pass2'] if 'pass2' in request.POST else ''
        

        if username == '' or email == '' or fname == '' or lname == '' or pass1 == '' or pass2 == '':
            return HttpResponse("403 - Something Went Wrong")
        

         # check for both password is same
        if (pass1!= pass2):
            messages.error(request, " Passwords not match")
            return redirect('home')

        # check for password is valid or not
        if not validatepassword(pass1):
            messages.error(request, " Your Passwords does not have in a describe format")
            return redirect('home')
        
        if not validatepassword(pass2):
            messages.error(request, " Your Passwords does not have in a describe format")
            return redirect('home')

        # check for username format
        if not validateusername(username):
            messages.error(request, " Your username does not have in a describe format")
            return redirect('home')

        
        
        # check for unique username
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                
                

                otp = generateOTP()
                numcode = generateNumCode()
                Emailotp.objects.create(username=username, fname=fname, lname=lname, email=email, passw=pass1, otp = otp, numcode=numcode)
                sendOTPEmail(otp, email)
                
                context = {'username' : username, 'fname' : fname, 'lname' : lname, 'email' : email, 'pass' : pass1, 'num' : numcode}
                return render(request, 'home/emailotp.html', context)

            else:
                messages.error(request, "Email-id already used, Choose different email")
                return redirect("home")
        else:
            messages.error(request, "Username not available")
            return redirect("home")
        
    else:
        return render(request, 'error/404.html')



def otpverifyemail(request):
    if request.method == 'POST':
        
        
        input_otp = request.POST['otp'] if 'otp' in request.POST else ''
        username = request.POST['username'] if 'username' in request.POST else ''
        email = request.POST['email'] if 'email' in request.POST else ''
        fname = request.POST['fname'] if 'fname' in request.POST else ''
        lname = request.POST['lname'] if 'lname' in request.POST else ''
        password = request.POST['pass'] if 'pass' in request.POST else ''
        code = request.POST['num'] if 'num' in request.POST else ''

        
        if input_otp == '' or username == '' or email == '' or fname == '' or lname == '' or password == '' or code == '':
            return HttpResponse('403 - Something Went Wrong')
        
        else:
            #print("Run")
            if input_otp.isdigit():
                inputotp = int(input_otp)

                otp_object = Emailotp.objects.filter(username=username, fname=fname, lname=lname, email=email, passw=password, numcode=code).last()


                otp_objectexist = True if otp_object else False   
                #print(otp_object)
                if otp_objectexist:

                    if not otp_object.IsExpired():

                        if inputotp == otp_object.otp:

                            myuser = User.objects.create_user(username, email, password)
                            myuser.first_name = fname
                            myuser.last_name = lname
                            myuser.is_active = True
                            myuser.save()

                            Account.objects.create(user=myuser)
                            
                            Emailotp.objects.filter(email__exact=email).delete()
                            Emailotp.objects.filter(username__exact=username).delete()
   
                            messages.success(request, "Congrats !! Your Account has been successfully created, Now you can login to your account")
                            return redirect('home')
                            
                        else:
                            context = {'username' : username, 'email':email, 'fname':fname, 'lname' : lname, 'pass' : password, 'num' : code}
                            messages.error(request, "You have entered the Wrong OTP !! Please Enter the correct otp ")
                            return render(request, 'home/emailotp.html', context)
                    else:
                        context = {'username' : username, 'email':email, 'fname':fname, 'lname' : lname, 'pass' : password, 'num' : code}
                        messages.error(request, "Your entered OTP is being Expired !!")
                        return render(request, 'home/emailotp.html', context)
                else:
                    return HttpResponse('403 - Something Went Wrong')
            else:
                context = {'username' : username, 'email':email, 'fname':fname, 'lname' : lname, 'pass' : password, 'num' : code}
                messages.error(request, "You have entered the Wrong OTP !! Please Enter the correct otp ")
                return render(request, 'home/emailotp.html', context)

    else:
        return HttpResponse("404 - Not found")





def loginprocess(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpass']

        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("home")

    return HttpResponse("404- Not found")


def logoutprocess(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')


def product(request, id, name):

    prodobj = Productitem.objects.filter(id=id).first()
    if prodobj:
        product = productpageData(prodobj)
        context = {'product' : product}
        return render(request, 'home/product.html', context)
    else:
        return HttpResponse("404 - Page Not found")
    



def profile(request, username):

    loggeduser = request.user

    if not loggeduser.is_anonymous and loggeduser.username == username:
        pass
    else:
        return HttpResponse("404 - Page Not found")

    if loggeduser.is_superuser:
        return render(request, 'home/profile.html') 


    try:
        userobj = User.objects.get(username=username)
        accountobj = Account.objects.filter(user=userobj).first()

        context = profilepageData(accountobj)

        return render(request, 'home/profile.html', context) 

    except User.DoesNotExist:
        return HttpResponse("404 - Page Not found")
    

def applyforseller(request):
    if request.method == 'POST':
        loguser = request.user

        if 'userfile' in request.FILES:
            document = request.FILES['userfile']
        else:
            return HttpResponse("Something went wrong")
        
        account = Account.objects.filter(user = loguser).first()

        if ApplyForSeller.objects.filter(account=account).exists():
            messages.warning(request, "You have already Submitted Application")
        else:
            ApplyForSeller.objects.create(account=account, document=document)
            messages.success(request, "Application Successfully Submitted")
        return redirect("profile", username=loguser.username)

        
    else:
        return HttpResponse("404 - page not found")


def allapplication(request, username):
    if request.method == 'POST':
        loguser = request.user
        if loguser.is_superuser and username == loguser.username:
            context = AdminConsoleApplication()
            return render(request, 'home/admin/allapplication.html', context) 
        else:
            return HttpResponse("404 - Not found")
    else:
        return HttpResponse("404 - Not found")


def sellerapprove(request):
    if request.method == 'POST':
        loguser = request.user
        if loguser.is_superuser:
            id = request.POST['id'] if 'id' in request.POST else ''

            if id == '':
                return HttpResponse("Something Went Wrong")


            obj = ApplyForSeller.objects.filter(id=id).first()
            obj.status = "approved"
            obj.account.role = "seller"
            obj.account.save()
            obj.save()

            messages.success(request, "Seller Application Approved")
            return redirect("profile", username=loguser.username)
        else:
            return HttpResponse("404 - page not found")

    else:
        return HttpResponse("404 - page not found")

def sellerreject(request):
    if request.method == 'POST':
        loguser = request.user
        if loguser.is_superuser:
            id = request.POST['id'] if 'id' in request.POST else ''
            if id == '':
                return HttpResponse("Something Went Wrong")

            obj = ApplyForSeller.objects.filter(id=id).first().delete()

            messages.success(request, "Seller Application Reject")
            return redirect("profile", username=loguser.username)
        else:
            return HttpResponse("404 - page not found")
    else:
        return HttpResponse("404 - page not found")


def allseller(request, username):
    if request.method == 'POST':
        loguser = request.user
        if loguser.is_superuser and username == loguser.username:
            context = AdminConsoleSeller()
            return render(request, 'home/admin/allseller.html', context) 
        else:
            return HttpResponse("404 - Not found")
    else:
        return HttpResponse("404 - Not found")

def allbuyer(request, username):
    if request.method == 'POST':
        loguser = request.user
        if loguser.is_superuser and username == loguser.username:
            context = AdminConsoleBuyer()
            return render(request, 'home/admin/allbuyer.html', context) 
        else:
            return HttpResponse("404 - Not found")
    else:
        return HttpResponse("404 - Not found")

def allproduct(request, username):
    if request.method == 'POST':
        loguser = request.user
        if loguser.is_superuser and username == loguser.username:
            context = AdminConsoleProduct()
            return render(request, 'home/admin/allproduct.html', context) 
        else:
            return HttpResponse("404 - Not found")
    else:
        return HttpResponse("404 - Not found")


def addproduct(request):
    if request.method == 'POST':
        name = request.POST['name'] if 'name' in request.POST else ''
        description = request.POST['description'] if 'description' in request.POST else ''
        quantity = request.POST['quantity'] if 'quantity' in request.POST else ''
        price = request.POST['price'] if 'price' in request.POST else ''
        category = request.POST['category'] if 'category' in request.POST else ''
        image1 = request.FILES['image1'] if 'image1' in request.FILES else '' 
        image2 = request.FILES['image2'] if 'image2' in request.FILES else ''

        if name == '' or description == '' or quantity == '' or price == '' or category == '' or image1 == '' or image2 == '':
            return HttpResponse("Something Went Wrong")
        
        loguser = request.user
        if loguser.is_anonymous:
            return HttpResponse("404 - Not found")
        else:
            accountobj = Account.objects.filter(user=loguser).first()
            if accountobj.role == 'seller':
                Productitem.objects.create(seller=accountobj, name=name, description=description, quantity=quantity, price=price, category=category, image1=image1, image2=image2)

                messages.success(request, "Product Item Added Successfully")
                return redirect("profile", username=loguser.username)
            else:
                return HttpResponse("404 - Not found")

    else:
        return HttpResponse("404 - Not found")


def sellerremove(request, username):
    if request.method == 'POST':
        loguser = request.user
        if loguser.is_superuser and loguser.username == username:
            id = request.POST['id'] if 'id' in request.POST else ''
            if id == '':
                return HttpResponse("Something Went Wrong")
            
            accountobj = Account.objects.filter(id=id).first()
            if accountobj and accountobj.role == 'seller':
                Productitem.objects.filter(seller=accountobj).delete()
                
                accountobj.role = 'buyer'
                accountobj.save()

                messages.success(request, "Seller Removed")
                return redirect("profile", username=loguser.username)
            else:
                return HttpResponse("Something Went Wrong")

        else:
            return HttpResponse("404 - Not found")
    else:
        return HttpResponse("404 - Not found")



def buyerremove(request, username):
    if request.method == 'POST':
        loguser = request.user
        if loguser.is_superuser and loguser.username == username:
            id = request.POST['id'] if 'id' in request.POST else ''
            if id == '':
                return HttpResponse("Something Went Wrong")
            
            accountobj = Account.objects.filter(id=id).first()
            if accountobj and accountobj.role == 'buyer':
                userobj = User.objects.filter(username=accountobj.user.username).first()

                userobj.delete()
                messages.success(request, "Buyer Removed")
                return redirect("profile", username=loguser.username)

            else:
                return HttpResponse("Something Went Wrong")
        else:
            return HttpResponse("404 - Not found")
    else:
        return HttpResponse("404 - Not found")



def productremove(request, username):
    if request.method == 'POST':
        loguser = request.user
        if loguser.is_superuser and loguser.username == username:
            id = request.POST['id'] if 'id' in request.POST else ''
            if id == '':
                
                return HttpResponse("Something Went Wrong")
            
            prodobj = Productitem.objects.filter(id=id).first()
            if prodobj:
                prodobj.delete()

                messages.success(request, "Product Removed")
                return redirect("profile", username=loguser.username)
            else:
                #print("Second")
                return HttpResponse("Something Went Wrong")
        else:
            return HttpResponse("404 - Not found")
    else:
        return HttpResponse("404 - Not found")



def sellercatalog(request):
    loguser = request.user

    if loguser.is_anonymous:
        return HttpResponse("404 - Not found")
    
    account = Account.objects.filter(user=loguser).first()
    if account and account.role == 'seller':
        productlist = []
        allprodobj = Productitem.objects.filter(seller=account)
        for prod in allprodobj:
            dt={}
            dt['id'] = prod.id
            dt['name'] = prod.name
            dt['quantity'] = prod.quantity
            dt['price'] = prod.price

            productlist.append(dt)
        
        return render(request, 'home/sellercatalog.html', {'productlist' : productlist})
    else:
        return HttpResponse("Something went wrong")



def sellereditproductpage(request):
    if request.method == 'POST':
        loguser = request.user

        if loguser.is_anonymous:
            return HttpResponse("404 - Not found")

        id = request.POST['id'] if 'id' in request.POST else ''
        if id == '':
            return HttpResponse("Something Went Wrong")
        prodobj = Productitem.objects.filter(id=id).first()

        if prodobj:
            if loguser == prodobj.seller.user:
                return render(request, 'home/selleredit.html', {'product' : prodobj})
            else:
                return HttpResponse("404 - Not found")
        else:    
            return HttpResponse("Something Went Wrong")


    else:
        return HttpResponse("404 - Not found")




def sellereditproduct(request):
    if request.method == 'POST':
        loguser = request.user

        if loguser.is_anonymous:
            return HttpResponse("404 - Not found")

        id = request.POST['id'] if 'id' in request.POST else ''
        name = request.POST['name'] if 'name' in request.POST else ''
        description = request.POST['description'] if 'description' in request.POST else ''
        quantity = request.POST['quantity'] if 'quantity' in request.POST else ''
        price = request.POST['price'] if 'price' in request.POST else ''
        category = request.POST['category'] if 'category' in request.POST else ''

        if id == '' or name == '' or description == '' or quantity == '' or price == '' or category == '':
            return HttpResponse("Something Went Wrong")
        prodobj = Productitem.objects.filter(id=id).first()
        
        if prodobj:
            if loguser == prodobj.seller.user:
                
                prodobj.name = name
                prodobj.description = description
                prodobj.quantity = quantity
                prodobj.price = price
                prodobj.category = category
                prodobj.save()

                messages.success(request, "Product Updated")
                return redirect("profile", username=loguser.username)
            else:
                return HttpResponse("404 - Not found")
        else:    
            return HttpResponse("Something Went Wrong")
    else:
        return HttpResponse("404 - Not found")
    
    
    

def sellerremoveproduct(request):
    if request.method == 'POST':
        loguser = request.user

        if loguser.is_anonymous:
            return HttpResponse("404 - Not found")

        id = request.POST['id'] if 'id' in request.POST else ''
        if id == '':
            return HttpResponse("Something Went Wrong")
        prodobj = Productitem.objects.filter(id=id).first()
        
        if prodobj:
            if loguser == prodobj.seller.user:
                prodobj.delete()

                messages.success(request, "Product Removed")
                return redirect("profile", username=loguser.username)
            else:
                return HttpResponse("404 - Not found")
        else:    
            return HttpResponse("Something Went Wrong")
    else:
        return HttpResponse("404 - Not found")

