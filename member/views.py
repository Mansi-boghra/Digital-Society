import re
from types import MemberDescriptorType
from django.http import HttpResponse
from django.shortcuts import redirect, render
from member.models import *

from secratory.models import Emergency, Member
from secratory.views import complain

# Create your views here.

def index(request):
    images = Gallery.objects.all()[2::-1]
    memcount = Member.objects.all().count()
    eventcount = Event.objects.all().count()
    complaincount = Complain.objects.all().count()

    try:
        uid = Member.objects.get(email=request.session['emails'])
        return render(request,'member-index.html',{'uid':uid,'images':images,'memcount':memcount,'eventcount':eventcount,'complaincount':complaincount})
    except:
        return render(request,'member-index.html',{'images':images,'memcount':memcount,'eventcount':eventcount,'complaincount':complaincount})



def member_blog_post (request):
    return render(request,'member-blog-post.html')

def member_blog (request):
    return render(request,'member-blog.html')

def logout (request):
    del request.session['emails']
    return redirect('member-login')

def member_contact (request):
    return render(request,'member-contact.html')  


def member_login(request):
    if request.method=='POST':
        try:
            uid=Member.objects.get(email=request.POST['email'])
            if request.POST['password']== uid.password:
                request.session['emails']=request.POST['email']
                return redirect('member-index')
            else:
                return render(request,'member-login.html',{'msg':'INVALID DATA'})
        except:
            msg='GO AND SIGNUP FIRST'
            return render(request,'member-login.html',{'msg':msg})
    return render(request,'member-login.html')

def member_change_password(request):
    uid = Member.objects.get(email=request.session['emails'])
    if request.method == 'POST':
        if uid.password == request.POST['opass']:
            if request.POST['npass'] == request.POST['cpass']:
                uid.password = request.POST['cpass']
                uid.save()
                return render(request,'member-change-password.html',{'msg':'Password has been updated'})
            return render(request,'member-change-password.html',{'msg':'New Password is not match'})
        return render(request,'member-change-password.html',{'msg':'Old Password is not correct'})
    return render(request,'member-change-password.html',{'uid':uid})

def member_gallery(request):
    uid = Member.objects.get(email=request.session['emails'])
    return render(request,'member-gallery.html',{'uid':uid})

def member_edit_profile(request):
    uid = Member.objects.get(email=request.session['emails'])
    # members = Member.objects.get
    if request.method == 'POST':
        uid.fname = request.POST['fname']
        uid.lname = request.POST['lname']
        # members.email = request.POST['email']
        uid.mobile = request.POST['mobile']
        uid.address = request.POST['address']
        if 'pic' in request.FILES:
            uid.pic = request.FILES['pic']
        # uid.flat_no = request.POST['flat_no']
        # uid.wing = request.POST['wing']
        # uid.doc_type = request.POST['doc']
        uid.save()
        msg='profile updated successfully'
        return render(request,'member-edit-profile.html',{'uid':uid,'msg':msg})
    return render(request,'member-edit-profile.html',{'uid':uid})

def contact_list(request):
    uid = Member.objects.get(email=request.session['emails'])
    contacts = Emergency.objects.all()
    return render(request,'contact-list.html',{'uid':uid,'contacts':contacts})

def member_complain(request):
    uid = Member.objects.get(email=request.session['emails'])
    if request.method=='POST':
            Complain.objects.create(
                complain_by = uid,
                subject = request.POST['subject'],
                des = request.POST['description'],
                # status = request.POST['status'],
            ) 
            msg = 'your complain send successfully'  
            complains = Complain.objects.all()[::-1]
            return render (request,'member-complain.html',{'msg':msg,'uid':uid,'complains':complains})
    else:
       msg='error'
       
    complains = Complain.objects.all()[::-1]
    return render (request,'member-complain.html',{'uid':uid,'complains':complains})

def member_my_complain(request):
    uid = Member.objects.get(email=request.session['emails'])
    complains = Complain.objects.filter(complain_by = uid)
    return render(request,'member-my-complain.html',{'uid':uid,'complains':complains})

def view_member_complain(request,pk):
    uid = Member.objects.get(email=request.session['emails'])
    complain = Complain.objects.get(id=pk)
    return render(request,'view-member-complain.html',{'uid':uid,'complain':complain})

def request_event(request):
    uid = Member.objects.get(email=request.session['emails'])
    return render(request,'request-event.html',{'uid':uid})

def view_event(request):
    uid = Member.objects.get(email=request.session['emails']) 
    events = Event.objects.all()[::-1]
    return render(request,'view-event.html',{'uid':uid,'events':events})

def member_maintenance(request):
    uid = Member.objects.get(email=request.session['emails'])
    return render(request,'member-maintenance.html',{'uid':uid})