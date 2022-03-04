from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('index/',views.index,name='index'),
    path('',views.signin,name='sign-in'),
    path('sign-up/',views.signup,name='sign-up'),
    path('profile/',views.profile,name='profile'),
    path('change-password/',views.change_password,name='change-password'),
    path('forgot-password/',views.forgot_password,name='forgot-password'),
    path('otp/',views.otp,name='otp'),
    path('logout/',views.logout,name='logout'),
    path('add-event/',views.add_event,name='add-event'),
    path('delete-event/<int:pk>',views.delete_event,name='delete-event'),
    path('edit-event/<int:pk>',views.edit_event,name='edit-event'),
    path('emergency-cont/',views.emergency_cont,name='emergency-cont'),
    path('delete-emergency-contact/<int:pk>',views.delete_emergency_contact,name='delete-emergency-contact'),
    path('manage-member/',views.manage_member,name='manage-member'),
    path('delete-member/<int:pk>',views.delete_member,name='delete-member'),
    path('edit-member/<int:pk>',views.edit_member,name='edit_member'),
    path('send-notice/',views.send_notice,name='send-notice'),
    path('gallery/',views.gallery,name='gallery'),
    path('complain/',views.complain,name='complain'),
    path('solve-complain/<int:pk>',views.solve_complain,name='solve-complain'),
    path('view-complain/<int:pk>',views.view_complain,name='view-complain'),
    path('maintenance/',views.maintenance,name='maintenance'),

    
]

