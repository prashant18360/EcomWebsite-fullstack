from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User 
from django.contrib.auth  import authenticate,  login, logout
from django.contrib import messages
from home.utility import *

# Create your views here.
def home(request):
    return render(request, 'home/home.html')
    #return HttpResponse("This is home")

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
                
                myuser = User.objects.create_user(username, email, pass1)
                myuser.first_name = fname
                myuser.last_name = lname
                myuser.is_active = True
                myuser.save()

                messages.success(request, "Congrats !! Your Account has been successfully created, Now you can login to your account")
                return redirect('home')
            else:
                messages.error(request, "Email-id already used, Choose different email")
                return redirect("home")
        else:
            messages.error(request, "Username not available")
            return redirect("home")
        
    else:
        return render(request, 'error/404.html')

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