from django.contrib import admin
from .models import *
# Register your models here.

# admin.site.register(AdminSec)

@admin.register(AdminSec)
class AdminSecModel(admin.ModelAdmin):
    list_display = ['name','email','mobile','created_at']

admin.site.register(Event)
admin.site.register(Member)
admin.site.register(Emergency)
