import re
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
    uid = AdminSec.objects.get(email=request.session['email'])
    if request.method == 'POST':
        # if 'pic' in request.FILES:
            Event.objects.create(
                uid = uid,
                title = request.POST['title'],
                des = request.POST['des'],
                event_at = request.POST['event_at'],
                # pic = request.FILES['pic'],
                pic = request.FILES['pic'] if 'pic' in request.FILES else None
            )
            msg = 'Event added successfully'
            events = Event.objects.all()[::-1]

            return render(request,'add-event.html',{'msg':msg,'uid':uid,'events':events})
        # else:
        #     Event.objects.create(
        #         uid = uid,
        #         title = request.POST['title'],
        #         des = request.POST['des'],
        #         event_at = request.POST['event_at']
        #     )
        #     msg = 'Event added successfully'
        #     return render(request,'add-event.html',{'msg':msg,'uid':uid})
    events = Event.objects.all()[::-1]
    return render(request,'add-event.html',{'uid':uid,'events':events})

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

def delete_event(request,pk):
    event = Event.objects.get(id=pk)
    event.delete()
    return redirect('add-event')

def edit_event(request,pk):
    uid = AdminSec.objects.get(email=request.session['email'])
    event = Event.objects.get(id=pk)
    date = str(event.event_at)
    if request.method == 'POST':
        event.title = request.POST['title']
        event.des = request.POST['des']
        event.event_at = request.POST['event_at']
        if 'pic' in request.FILES:
            event.pic = request.FILES['pic']
        event.save()
        return redirect('add-event')
    return render(request,'edit-event.html',{'uid':uid,'event':event,'date':date})
