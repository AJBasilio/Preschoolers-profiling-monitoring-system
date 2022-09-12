from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import *
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
            print(user_email, password)
            user = authenticate(request, email=user_email, password=password)
            print(user.user_type)

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
    return render(request, 'activities/Admin Home.html')

# ===== BHW =====
@login_required(login_url='login_registration')
def bhw_home(request):
    return render(request, 'activities/BHW Home.html')