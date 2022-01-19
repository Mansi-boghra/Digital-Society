from django.http.response import HttpResponse
from django.shortcuts import redirect, render

from .models import *
from random import randrange
from django.conf import settings
from django.core.mail import send_mail


# Create your views here.


def index(request):
    return render(request,'index.html')

def signin(request):
    if request.method == 'POST':
        try:
            uid = AdminSec.objects.get(email = request.POST['email'])
            if request.POST['password'] == uid.password:
                request.session['email'] = request.POST['email']
                return render(request,'index.html')
            return render(request,'sign-in.html',{'msg':'Incorrect password'})
        except:
            msg = 'Email is not register'
            return render(request,'sign-up.html',{'msg':msg})

    return render(request,'sign-in.html')

def signup(request):
    if request.method == 'POST':
        try:
            AdminSec.objects.get(email=request.POST['email'])
            msg = 'Email is already register'
            return render(request,'sign-in.html',{'msg':msg})
        except:
             if len(request.POST['password']) > 7:
                if request.POST['password'] == request.POST['cpassword']:
                    otp = randrange(1000,9999)
                    subject = 'Account Verification'
                    message = f'Your OTP is : {otp}'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [request.POST['email'], ]
                    send_mail( subject, message, email_from, recipient_list )
                    global temp
                    temp = {
                        'name' : request.POST['name'],
                        'email' : request.POST['email'],
                        'mobile' : request.POST['mobile'],
                        'address' : request.POST['address'],
                        'password' : request.POST['password'],
                    }
                    return render(request,'otp.html',{'otp':otp})
                return render(request,'sign-up.html',{'msg':'password does not match'})
             return render(request,'sign-up.html',{'msg':'enter minimum 8 character'})
    return render(request,'sign-up.html')

def profile(request):
    return render(request,'profile.html')

def forgot_password(request):
    return render(request,'forgot-password.html')

def otp(request):
    if request.method == 'POST':
        if request.POST['otp'] == request.POST['uotp']:
            global temp
            AdminSec.objects.create(
                name = temp['name'],
                email = temp['email'],
                mobile = temp['mobile'],
                address = temp['address'],
                password = temp['password']
            )
            msg = 'Account Created'
            return render(request,'sign-in.html',{'msg':msg})
        else:
            msg = 'Invalid OTP'
            return render(request,'otp.html',{'msg':msg,'otp':request.POST['otp']})
    # return render(request,'otp.html')


def logout(request):
    del request.session['email']
    return redirect('sign-in')