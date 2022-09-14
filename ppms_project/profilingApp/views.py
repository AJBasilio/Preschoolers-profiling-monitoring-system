from ast import dump
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import *
from .models import *
from json import dumps
# Create your views here.

def index(request):
    return HttpResponse('Hello World')

@unauthenticated_user
def login_registration(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        if 'register_btn' in request.POST:
            form = CustomUserCreationForm(request.POST)
            
            if form.is_valid():
                form.save()
                return redirect('login_registration')
        else:
            user_email = request.POST.get('email')
            password = request.POST.get('password')

            user = authenticate(request, email=user_email, password=password)

            if user is not None and user.user_type == 'P/G':
                login(request, user)
                return redirect('parent_home')
            elif user is not None and user.user_type == 'BHW':
                login(request, user)
                return redirect('bhw_home')
            elif user is not None and user.user_type == 'Admin':
                login(request, user)
                return redirect('admin_home')

    context = {'form' : form}
    return render(request, 'activities/login_registration.html', context)

def logout_user(request):
    logout(request)
    return redirect('login_registration')

# ===== PARENT =====
@login_required(login_url='login_registration')
def parent_home(request):
    return render(request, 'activities/Parent Home.html')

# ===== ADMIN =====
@login_required(login_url='login_registration')
def admin_home(request):
    validated_status = BarangayHealthWorker.objects.filter(is_validated=True).count()
    invalidated_status = BarangayHealthWorker.objects.filter(is_validated=False).count()
    parent_count = Parents.objects.all().count()
    preschooler_count = Preschoolers.objects.all().count()

    count_list = [validated_status, invalidated_status, parent_count, preschooler_count]
    data_json = dumps(count_list)

    context = {'validated_count' : validated_status,
                'invalidated_count' : invalidated_status,
                'parent_count' : parent_count,
                'preschooler_count' : preschooler_count,
                'count_data' : data_json}
                
    return render(request, 'activities/Admin Home.html', context)

def bhw_validation(request):
    return render(request, 'activities/Admin Validate BHW.html')

# ===== BHW =====
@login_required(login_url='login_registration')
def bhw_home(request):
    return render(request, 'activities/BHW Home.html')

def preschooler_profile(request):
    context = {}
    return render(request, 'activities/BHW Preschooler Profile.html', context)

def immunization_schedule(request):
    return render(request, 'activities/BHW Immunization Schedule.html')