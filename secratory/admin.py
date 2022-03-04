from django.contrib import admin
from .models import *
# Register your models here.

# admin.site.register(AdminSec)

@admin.register(AdminSec)
class AdminSecModel(admin.ModelAdmin):
    list_display = ['name','email','mobile','created_at']

@admin.register(Event)
class EventModel(admin.ModelAdmin):
    list_display = ['title','des','event_at','created_at']

@admin.register(Member)
class MemberModel(admin.ModelAdmin):
    list_display = ['fname','lname','email','mobile','flat_no','wing','doc_type','doc_num','create_at']

@admin.register(Emergency)
class EmergencyModel(admin.ModelAdmin):
    list_display = ['name','occup','contact','email']

admin.site.register(Gallery)

@admin.register(Maintenance)
class MaintenanceModel(admin.ModelAdmin):
    list_display = ['pay_by','amount','pay_time','month','year','pay_id']



