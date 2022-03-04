from unicodedata import name
from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name='member-index'),
    path('member-blog-post/',views.member_blog_post,name='member-blog-post'),
    path('member-blog/',views.member_blog,name='member-blog'),
    path('member-contact/',views.member_contact,name='member-contact'),
    path('member-login/',views.member_login,name='member-login'),
    path('member-change-password/',views.member_change_password,name='member-change-password'),
    path('logout/',views.logout,name='logout'),
    path('member-gallery/',views.member_gallery,name='member-gallery'),
    path('member-edit-profile/',views.member_edit_profile,name='member-edit-profile'),
    path('contact-list/',views.contact_list,name='contact-list'),
    path('member-complain/',views.member_complain,name='member-complain'),
    path('member-my-complain/',views.member_my_complain,name='member-my-complain'),
    path('view-member-complain/<int:pk>',views.view_member_complain,name='view-member-complain'),
    path('request-event/',views.request_event,name='request-event'),
    path('view-event/',views.view_event,name='view-event'),
    path('member-maintenance/',views.member_maintenance,name='member-maintenance'),

    







]