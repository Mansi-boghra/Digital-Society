from calendar import month
from django.db import models

# Create your models here.

class AdminSec(models.Model):

    name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    pic = models.FileField(upload_to='Admin Profile',default='avtar.jpg')

    def __str__(self):
        return self.name + ' @ ' + self.email


class Event(models.Model):

    uid = models.ForeignKey(AdminSec,on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    des = models.TextField()
    event_at = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    pic = models.FileField(upload_to='Event',null=True,blank=True)

    def __str__(self):
        return self.title

class Emergency(models.Model):

    uid = models.ForeignKey(AdminSec,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    occup = models.CharField(max_length=30)
    contact = models.CharField(max_length=15)
    email = models.EmailField(null=True,blank=True)

    def __str__(self):
        return self.name

class Member(models.Model):

    uid = models.ForeignKey(AdminSec,on_delete=models.CASCADE)
    fname = models.CharField(max_length=15)
    lname = models.CharField(max_length=15)
    
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    password = models.CharField(max_length=20)
    pic = models.FileField(upload_to='member',default='avtar.jpg')
    flat_no = models.IntegerField()
    wing = models.CharField(max_length=2)
    address = models.TextField(null=True,blank=True)
    doc_type = models.CharField(max_length=20)
    doc_num = models.CharField(max_length=20)
    create_at = models.DateTimeField(auto_now_add=True)
    role = models.BooleanField(default=True)

    def __str__(self):
        return self.fname + '   ' + self.lname

class Gallery(models.Model):

    choices = (('garden','garden'),('gym','gym'),('events','events'),('society','society'))

    uid = models.ForeignKey(AdminSec,on_delete=models.CASCADE)
    type = models.CharField(max_length=20,choices=choices,default='events')
    pic = models.FileField(upload_to='gallery')

    def __str__(self):
        return self.uid.name + '  ' + str(self.pic.url)

# class Maintenance(models.Model):

#     pay_by = models.ForeignKey(AdminSec,on_delete=models.CASCADE)
#     amount = models.IntegerField(default=0)
#     pay_time = models.DateTimeField(auto_now_add=True)
#     month = models.CharField(max_length=15)
#     year = models.IntegerField()
#     pay_id = models.CharField(max_length=20,unique=True)

#     def __str__(self):
        return self.pay_by.fname + ' ' + self.pay_by.lname
