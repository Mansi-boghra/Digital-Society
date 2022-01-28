from urllib import request
from django.http.response import HttpResponse
from django.shortcuts import redirect, render

from .models import *
from random import randrange, choices
from django.conf import settings
from django.core.mail import send_mail


# Create your views here.


def index(request):
    try:
        uid = AdminSec.objects.get(email=request.session['email'])
        return render(request,'index.html',{'uid':uid})
    except:
        pass
    return render(request,'index.html')

def signin(request):
    try:
        AdminSec.objects.get(email=request.session['email'])
        return redirect('index')
    except:
        if request.method == 'POST':
            try:
                uid = AdminSec.objects.get(email = request.POST['email'])
                if request.POST['password'] == uid.password:
                    request.session['email'] = request.POST['email']
                    return redirect('index')
                return render(request,'sign-in.html',{'msg':'Incorrect password'})
            except:
                msg = 'Email is not Register'
                return render(request,'sign-up.html',{'msg':msg})

        return render(request,'sign-in.html')

def signup(request):
    if request.method == 'POST':
        try:
            AdminSec.objects.get(email=request.POST['email'])
            msg = 'Your email is already exist'
            return render(request,'sign-in.html',{'msg':msg})
        except:
            if len(request.POST['password']) > 7:
                if request.POST['password'] == request.POST['cpassword']:
                    otp = randrange(1000,9999)
                    subject = 'Account Verification'
                    message = f'Your verification OTP is : {otp}'
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
    uid = AdminSec.objects.get(email=request.session['email'])
    if request.method == 'POST':
        uid.name = request.POST['name']
        uid.mobile = request.POST['mobile']
        uid.address = request.POST['address']
        msg = 'profile updated'
        uid.save()
        return render(request,'profile.html',{'msg':msg,'uid':uid})
    return render(request,'profile.html',{'uid':uid})



def forgot_password(request):
    if request.method == 'POST':
        try:
            uid = AdminSec.objects.get(email=request.POST['email'])
            s = 'qwertyuio12346586'
            password = ''.join(choices(s,k=8))
            
            subject = 'Password forgot'
            message = f'Your Password is : {password}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.POST['email'], ]
            send_mail( subject, message, email_from, recipient_list )
            msg = 'Email sent'
            uid.password = password
            uid.save()
            return render(request,'forgot-password.html',{'msg':msg})

        except:
            msg = 'Email is not register'
            return render(request,'forgot-password.html',{'msg':msg})
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

def add_event(request):
    # if 'pic' in request.FILES
    # request.FILES['pic']
    return render (request,'Add-event.html')


def change_password(request):
    uid = AdminSec.objects.get(email=request.session['email'])
    if request.method == 'POST':
        if uid.password == request.POST['opass']:
            if request.POST['npass'] == request.POST['cpass']:
                uid.password = request.POST['cpass']
                uid.save()
                return render(request,'change-password.html',{'msg':'Password has been updated'})
            return render(request,'change-password.html',{'msg':'New Password is not match'})
        return render(request,'change-password.html',{'msg':'Old Password is not correct'})
    return render(request,'change-password.html')