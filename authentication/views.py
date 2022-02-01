from email import message
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from loginpage import settings
from django.core.mail import send_mail

# Create your views here.

def home(request):
    return render(request, 'authentication/index.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request, "Your account has been successfully created.")

        # welcome email :

        subject = "Welcome to my projoect"
        message = "Hello" + myuser.first_name + " !! \n"+ " Thanks to try my project \n" +"Please confirm you inbox in order to activate your account" 
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)    

        return redirect('signin')

    return render(request, 'authentication/signup.html')


def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            return render(request, 'authentication/signout.html')
        else:
            messages.error(request, 'Incorrect Credantials')  
            return redirect('home')  

    return render(request, 'authentication/signin.html')

def signout(request):
    logout(request)
    messages.success(request, "Logged Out successfully !!")
    return redirect('home')