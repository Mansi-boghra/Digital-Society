from django.db import models
from secratory.models import *

# Create your models here.

class Notice(models.Model):
    
    send_by = models.ForeignKey(AdminSec,on_delete=models.CASCADE)
    rec_by = models.ForeignKey(Member,on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    des = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

class Complain(models.Model):

    complain_by = models.ForeignKey(Member,on_delete=models.CASCADE)
    solve_by = models.ForeignKey(AdminSec,on_delete=models.CASCADE,null=True,blank=True)
    subject = models.CharField(max_length=80)
    des = models.TextField()
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    solved_at = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.subject + '  ' + self.complain_by.fname


    

