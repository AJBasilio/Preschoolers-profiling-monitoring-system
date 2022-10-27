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
    path('ahome2', views.admin_home2, name='admin_home2'),
    path('validation', views.bhw_validation, name='bhw_validation'),
    path('validate_profile/<str:pk>/', views.unvalidated_profile, name='unvalidated_profile'),
    path('delete_profile/<str:pk>/', views.delete_profile, name='delete_profile'),


    # Barangay Health Worker
    path('bhome', views.bhw_home, name='bhw_home'),
    path('preschooler_profile', views.preschooler_profile, name='preschooler_profile'),
    path('preschooler_dashboard', views.preschooler_dashboard, name='preschooler_dashboard'),
    path('update_preschooler', views.update_preschooler, name='update_preschooler'),
    path('immunization', views.immunization_schedule, name='immunization_schedule'),
]