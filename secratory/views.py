from datetime import datetime
import re
from urllib.request import Request
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import *
from random import randrange, choices
from django.conf import settings
from django.core.mail import send_mail
from member import models as mm

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
    return render(request,'change-password.html',{'uid':uid})

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

def emergency_cont(request):
    uid = AdminSec.objects.get(email=request.session['email'])
    if request.method == 'POST':
            Emergency.objects.create(
                uid = uid,
                name = request.POST['name'],
                occup = request.POST['occup'],
                contact = request.POST['contact'],   
                email = request.POST['email'], 
            )
            msg = 'Emergency-contact added successfully'
            contacts = Emergency.objects.all()[::-1]

            return render(request,'emergency-cont.html',{'msg':msg,'uid':uid,'contacts':contacts})
    contacts = Emergency.objects.all()[::-1]
    return render(request,'emergency-cont.html',{'uid':uid,'contacts':contacts})

def delete_emergency_contact(request,pk):
    emer = Emergency.objects.get(id=pk)
    emer.delete()
    return redirect('emergency-cont')

def manage_member(request):
    uid = AdminSec.objects.get(email=request.session['email'])
    if request.method == 'POST':
        try:
            Member.objects.get(email=request.POST['email'])
            msg = 'Member already created with this email'
            return render(request,'manage-member.html',{'uid':uid,'msg':msg})
        except:
            s = 'ABqwweirtuioplkjhgfdsazxcvbnm123467890'
            password = ''.join(choices(s,k=8))
            Member.objects.create(
                uid = uid,
                fname = request.POST['fname'],
                lname = request.POST['lname'],
                email = request.POST['email'],
                password = password,
                mobile = request.POST['mobile'],
                flat_no = request.POST['flat_no'],
                wing = request.POST['wing'],
                address = request.POST['address'],
                doc_type = request.POST['doc'],
                doc_num = request.POST['dnumber'],
                role = True if 'verify' in request.POST else False
            )
            msg = 'member added successfully'
            members = Member.objects.all()[::-1]

            subject = 'New member! your account is created'
            message = f"""Hello {request.POST['fname']}!!
            Your society account is created .
            User id : {request.POST['email']}
            password : {password}
            plaese change the password after login.
            """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.POST['email'], ]
            send_mail( subject, message, email_from, recipient_list )
            
            return render(request,'manage-member.html',{'uid':uid,'msg':msg,'members':members})
    members = Member.objects.all()[::-1]
    return render(request,'manage-member.html',{'uid':uid,'members':members})

def delete_member(request,pk):
    member = Member.objects.get(id=pk)
    member.delete()
    return redirect('manage-member')

def edit_member(request,pk):
    uid = AdminSec.objects.get(email=request.session['email'])
    members = Member.objects.get(id=pk)
    if request.method == 'POST':
        members.fname = request.POST['fname']
        members.lname = request.POST['lname']
        # members.email = request.POST['email']
        members.mobile = request.POST['mobile']
        members.wing = request.POST['wing']
        members.doc_type = request.POST['doc']
        members.save()
        return redirect('manage-member')
    return render(request,'edit_member.html',{'uid':uid,'members':members})


def send_notice(request):
    uid = AdminSec.objects.get(email=request.session['email'])
    members = Member.objects.all()
    if request.method == 'POST':
        mm.Notice.objects.create(
            send_by = uid,
            rec_by = Member.objects.get(email=request.POST['send-to']),
            subject = request.POST['subject'],
            des = request.POST['des'],
        )
        notice = mm.Notice.objects.all()
        subject = 'Notice alert'
        message = f""" view notice """
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [request.POST['send-to'], ]
        send_mail( subject, message, email_from, recipient_list )

        return render(request,'send-notice.html',{'uid':uid,'members':members,'notice':notice,'msg':'Notice is sent'}) 
    notice = mm.Notice.objects.all()
    return render(request,'send-notice.html',{'uid':uid,'members':members,'notices':notice})

def delete_notice(request,pk):
    notice = mm.Notice.objects.get(id=pk)
    notice.delete()
    return redirect('send-notice')

def gallery(request):
    # msg = 'Photo added successfully'
    uid = AdminSec.objects.get(email=request.session['email'])
    if request.method == 'POST':
        # if 'pic' in request.FILES:
            Gallery.objects.create(
                uid = uid,
                pic = request.FILES['pic'],
                type = request.POST['types'],
                
            )
            msg = 'Photo added successfully'
            return render(request,'gallery.html',{'uid':uid,'msg':msg}) 
    return render(request,'gallery.html',{'uid':uid})

def complain(request):
    uid = AdminSec.objects.get(email=request.session['email'])
    complains = mm.Complain.objects.all()
    return render(request,'complain.html',{'uid':uid,'complains':complains})

def solve_complain(request,pk):
    uid = AdminSec.objects.get(email=request.session['email'])
    complain = mm.Complain.objects.get(id=pk)
    complain.status = True
    complain.solve_by = uid
    complain.solved_at = datetime.now()
    complain.save()
    subject = 'Complain'
    message = f""" Your complain is solve,view in app for more details...  """
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [complain.complain_by.email ]
    send_mail( subject, message, email_from, recipient_list )
    return redirect('complain') 

def view_complain(request,pk):
    uid = AdminSec.objects.get(email=request.session['email'])
    complains = mm.Complain.objects.get(id=pk)
    return render(request,'view-complain.html',{'uid':uid,'complains':complains})

def maintenance(request):
    uid = AdminSec.objects.get(email=request.session['email'])
    main = mm.Maintenance.objects.all()
    return render(request,'maintenance.html',{'uid':uid,'main':main})
