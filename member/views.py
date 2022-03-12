from django.http import HttpResponse
from django.shortcuts import redirect, render
from member.models import *
from secratory.models import Emergency, Member
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

from secratory.views import maintenance
# Create your views here.

def index(request):
    images = Gallery.objects.all()[20::-1]
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
    photos = Gallery.objects.all()[::-1]
    return render(request,'member-gallery.html',{'uid':uid,'photos':photos})

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

def pending_request(request):
    uid = Member.objects.get(email=request.session['emails'])
    events = Event.objects.all()
    return render(request,'pending-request.html',{'uid':uid,'events':events})

def member_maintenance(request):
    uid = Member.objects.get(email=request.session['emails'])
    if request.method == 'POST':
        main = Maintenance.objects.create(
            pay_by = uid,
            amount = request.POST['amount'],
            month = request.POST['month']+'-01'
        )    
        currency = 'INR'
        amount = 200000  # Rs. 200
    
        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                        currency=currency,
                                                        payment_capture='0'))
    
        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = f'paymenthandler/{main.id}'
    
        # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url
        context['uid'] = uid
        context['main'] = main
        return render(request,'pay.html',context=context)
    return render(request,'member-maintenance.html',{'uid':uid})

def pay_maintenance(request):
    uid = Member.objects.get(email=request.session['emails'])
    main = Maintenance.objects.filter(verify=True)[::-1]
    return render(request,'pay-maintenance.html',{'uid':uid,'main':main})

def member_notice(request):
    uid = Member.objects.get(email=request.session['emails'])
    return render(request,'member-notice.html',{'uid':uid})


# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
 
 
# def homepage(request):
#     currency = 'INR'
#     amount = 20000  # Rs. 200
 
#     # Create a Razorpay Order
#     razorpay_order = razorpay_client.order.create(dict(amount=amount,
#                                                        currency=currency,
#                                                        payment_capture='0'))
 
#     # order id of newly created order.
#     razorpay_order_id = razorpay_order['id']
#     callback_url = 'paymenthandler/'
 
#     # we need to pass these details to frontend.
#     context = {}
#     context['razorpay_order_id'] = razorpay_order_id
#     context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
#     context['razorpay_amount'] = amount
#     context['currency'] = currency
#     context['callback_url'] = callback_url
 
#     return render(request, 'index.html', context=context)
 
 
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request,pk):
    main = Maintenance.objects.get(id=pk)
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            # if result is None:
            amount = 200000  # Rs. 200
            try:

                # capture the payemt
                razorpay_client.payment.capture(payment_id, amount)
                main.verify = True
                main.pay_id = payment_id
                main.save()
                # render success page on successful caputre of payment
                return render(request, 'success.html',{'main':main})
            except:

                # if there is an error while capturing payment.
                return render(request, 'fail.html')
            # else:
 
            #     # if signature verification fails.
            #     return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()

