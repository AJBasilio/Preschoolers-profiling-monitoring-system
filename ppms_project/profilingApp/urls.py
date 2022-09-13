from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.login_registration, name='login_registration'),
    path('logout', views.logout_user, name='logout'),

    # Parent
    path('home', views.parent_home, name='parent_home'),

    # Admin
    path('ahome', views.admin_home, name='admin_home'),
    path('validation', views.bhw_validation, name='bhw_validation'),

    # Barangay Health Worker
    path('bhome', views.bhw_home, name='bhw_home'),
    path('preschoolers', views.preschooler_profile, name='preschooler_profile'),
    path('immunization', views.immunization_schedule, name='immunization_schedule'),
]