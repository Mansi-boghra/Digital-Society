from django.urls import path
from . import views

urlpatterns = [
    path('index/',views.index,name='index'),
    path('',views.signin,name='sign-in'),
    path('sign-up/',views.signup,name='sign-up'),
    path('profile/',views.profile,name='profile'),
    path('forgot-password/',views.forgot_password,name='forgot-password'),
    path('otp/',views.otp,name='otp'),
    path('logout/',views.logout,name='logout'),
]

