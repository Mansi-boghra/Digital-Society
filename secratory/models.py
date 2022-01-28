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
