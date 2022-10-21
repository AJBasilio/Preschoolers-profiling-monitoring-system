from ast import dump
from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import *
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
                messages.success(request, 'Your account is successfully created.')
                form.save()
            else:
                error_string = ''.join([''.join(x for x in l) for l in list(form.errors.values())])
                messages.error(request, str(error_string))
          
        else:
            user_email = request.POST.get('email')
            password = request.POST.get('password')

            user = authenticate(request, email=user_email, password=password)

            if user is not None and user.user_type == 'P/G':

                login(request, user)
                return redirect('parent_home')

            elif user is not None and user.user_type == 'BHW':

                bhw_validation_status = BarangayHealthWorker.objects.get(user=user)
                if bhw_validation_status.is_validated:
                    login(request, user)
                    return redirect('bhw_home')
                else:
                    # Error message pop-up
                    messages.warning(request, 'Please wait for the validation.')

            elif user is not None and user.user_type == 'Admin':
                
                login(request, user)
                return redirect('admin_home')
            
            else:
                messages.error(request, 'Login Failed')

    context = {'form' : form}
    return render(request, 'activities/login_registration.html', context)

def logout_user(request):
    logout(request)
    return redirect('login_registration')

# ================================== PARENTS/GUARDIANS ==================================
@login_required(login_url='login_registration')
def parent_home(request):
    parent_user = Parent.objects.get(user_id=request.user.id)
    preschooler = Preschooler.objects.filter(parent=parent_user)

    if request.method == 'POST':
        parent = parent_user
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        suffix_name = request.POST.get('suffix_name')
        birthday = request.POST.get('birthday')

        psa = Preschooler.objects.create(parent=parent,
                                        first_name=first_name,
                                        middle_name=middle_name,
                                        last_name=last_name,
                                        suffix_name=suffix_name,
                                        birthday=birthday
                                        )
        return redirect('parent_home')

    context = {'preschoolers' : preschooler}
    return render(request, 'activities/Parent Home.html', context)

# ================================== ADMIN ==================================
@login_required(login_url='login_registration')
def admin_home(request):
    validated_status = BarangayHealthWorker.objects.filter(is_validated=True).count()
    invalidated_status = BarangayHealthWorker.objects.filter(is_validated=False).count()
    parent_count = Parent.objects.all().count()
    preschooler_count = Preschooler.objects.all().count()

    count_list = [validated_status, invalidated_status, parent_count, preschooler_count]
    data_json = dumps(count_list)

    context = {'validated_count' : validated_status,
                'invalidated_count' : invalidated_status,
                'parent_count' : parent_count,
                'preschooler_count' : preschooler_count,
                'count_data' : data_json}
                
    return render(request, 'activities/Admin Home.html', context)

def bhw_validation(request):
    bhw = BarangayHealthWorker.objects.all()

    context = {'bhws' : bhw}
    return render(request, 'activities/Admin Validate BHW.html', context)

def admin_home2(request):
    return render(request, 'activities/Admin Home2.html')

def unvalidated_profile(request, pk):
    unvalidate_bhw = BarangayHealthWorker.objects.get(user_id=pk)
    form = Validate_BHW(instance=unvalidate_bhw)
    
    if request.method == 'POST':
        form = Validate_BHW(request.POST, instance=unvalidate_bhw)
        if form.is_valid():
            form.save()
            return redirect('bhw_validation')

    context = {'bhw' : unvalidate_bhw,
               'form' : form}
    return render(request, 'activities/Unvalidated Profile.html', context)

def delete_profile(request, pk):
    delete_bhw = BarangayHealthWorker.objects.get(user_id=pk)
    user_bhw = CustomUser.objects.get(id=pk)

    if request.method == 'POST':

        user_bhw.delete()
        
        return redirect('bhw_validation')

    context = {'bhw' : delete_bhw}
    return render(request, 'activities/Admin Delete Confirmation.html', context)

# ================================== BHW ==================================
@login_required(login_url='login_registration')
def bhw_home(request):
    return render(request, 'activities/BHW Home.html')

def preschooler_profile(request):
    context = {}
    return render(request, 'activities/BHW Preschooler Profile.html', context)

def immunization_schedule(request):
    return render(request, 'activities/BHW Immunization Schedule.html')
