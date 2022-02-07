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
   
]

