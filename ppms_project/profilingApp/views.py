from itertools import count
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
                messages.success(
                    request, 'Your account is successfully created.')
                form.save()
            else:
                CRITICAL = 50
                error_string = ''.join([''.join(x for x in l)
                                       for l in list(form.errors.values())])
                messages.add_message(request, CRITICAL, str(error_string))

        else:
            user_email = request.POST.get('email')
            password = request.POST.get('password')

            user = authenticate(request, email=user_email, password=password)
            if user is not None and user.user_type == 'P/G':
                login(request, user)
                return redirect('parent_home')
            elif user is not None and user.user_type == 'BHW':
                bhw_validation_status = BarangayHealthWorker.objects.get(
                    user=user)
                if bhw_validation_status.is_validated:
                    login(request, user)
                    return redirect('bhw_home')
                else:
                    # Error message pop-up
                    messages.warning(
                        request, 'Please wait for the validation.')
            elif user is not None and user.user_type == 'Admin':
                login(request, user)
                return redirect('admin_home')
            else:
                messages.error(request, 'Login Failed')

    context = {'form': form}
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
        if request.POST.get('suffix_name') is None:
            suffix_name = None
        else:
            suffix_name = request.POST.get('suffix_name')
        birthday = request.POST.get('birthday')
        gender = request.POST.get('gender')

        psa = Preschooler.objects.create(parent=parent,
                                         first_name=first_name,
                                         middle_name=middle_name,
                                         last_name=last_name,
                                         suffix_name=suffix_name,
                                         birthday=birthday,
                                         gender=gender
                                         )
        return redirect('parent_home')

    context = {'preschoolers': preschooler}
    return render(request, 'activities/Parent Home.html', context)

def parent_preschooler(request, pk):
    preschooler = Preschooler.objects.get(id=pk)

    context = {'preschooler' : preschooler}
    return render(request, 'activities/Parent - Preschooler Profile.html', context)
# ================================== ADMIN ==================================


@login_required(login_url='login_registration')
def admin_home(request):
    all_bhw = BarangayHealthWorker.objects.all()
    validated_status = BarangayHealthWorker.objects.filter(
        is_validated=True).count()
    invalidated_status = BarangayHealthWorker.objects.filter(
        is_validated=False).count()
    parent_count = Parent.objects.all().count()
    preschooler_count = Preschooler.objects.all().count()

    count_list = [validated_status, invalidated_status,
                  parent_count, preschooler_count]
    data_json = dumps(count_list)

    context = {'bhws': all_bhw,
               'validated_count': validated_status,
               'invalidated_count': invalidated_status,
               'parent_count': parent_count,
               'preschooler_count': preschooler_count,
               'count_data': data_json}

    return render(request, 'activities/Admin Home.html', context)


def bhw_validation(request):
    bhw = BarangayHealthWorker.objects.filter(is_validated=False)
    invalidated_status = BarangayHealthWorker.objects.filter(
        is_validated=False).count()
    context = {'bhws': bhw, 
               'invalidated_count': invalidated_status,}

    return render(request, 'activities/Admin Validate BHW.html', context)


def admin_preschoolers(request):
    invalidated_status = BarangayHealthWorker.objects.filter(
        is_validated=False).count()

    preschooler_normal = []
    preschooler_wasted = []
    preschooler_severly = []
    preschooler_over_obese = []

    for obj in Preschooler.objects.all():
        if obj.bmi_tag == 'NORMAL':
            preschooler_normal.append(obj)
        elif obj.bmi_tag == 'ABOVE NORMAL':
            preschooler_over_obese.append(obj)
        elif obj.bmi_tag == 'BELOW NORMAL':
            preschooler_wasted.append(obj)
        else:
            preschooler_severly.append(obj)

    normal_count = len(preschooler_normal)
    wasted_count = len(preschooler_wasted)
    severly_count = len(preschooler_severly)
    overobese_count = len(preschooler_over_obese)

    count_list = [normal_count, wasted_count, severly_count, overobese_count, overobese_count]
    data_json = dumps(count_list)
    
    context = {'invalidated_count': invalidated_status,
               'normal' : normal_count,
               'wasted' : wasted_count,
               'severly' : severly_count,
               'overobese' : overobese_count,
               'count_data' : data_json}

    return render(request, 'activities/Admin - Preschooler.html', context)

def admin_preschoolers_barangay(request, brgy):
    invalidated_status = BarangayHealthWorker.objects.filter(
        is_validated=False).count()

    parents = Parent.objects.filter(barangay=brgy)
    preschoolers = Preschooler.objects.filter(parent__in=(parents))

    preschooler_normal = []
    preschooler_wasted = []
    preschooler_severly = []
    preschooler_over_obese = []

    for p in preschoolers:
        if p.bmi_tag == 'NORMAL':
            preschooler_normal.append(p)
        elif p.bmi_tag == 'ABOVE NORMAL':
            preschooler_over_obese.append(p)
        elif p.bmi_tag == 'BELOW NORMAL':
            preschooler_wasted.append(p)
        else:
            preschooler_severly.append(p)
    
    normal_count = len(preschooler_normal)
    wasted_count = len(preschooler_wasted)
    severly_count = len(preschooler_severly)
    overobese_count = len(preschooler_over_obese)

    count_list = [normal_count, wasted_count, severly_count, overobese_count, overobese_count]
    data_json = dumps(count_list)

    context = {'invalidated_count': invalidated_status,
               'brgy' : brgy,
               'normal' : normal_count,
               'wasted' : wasted_count,
               'severly' : severly_count,
               'overobese' : overobese_count,
               'count_data' : data_json
               }

    return render(request, 'activities/Admin - Preschooler_barangay.html', context)

def unvalidated_profile(request, pk):
    unvalidate_bhw = BarangayHealthWorker.objects.get(user_id=pk)
    form = Validate_BHW(instance=unvalidate_bhw)

    if request.method == 'POST':
        form = Validate_BHW(request.POST, instance=unvalidate_bhw)
        if form.is_valid():
            form.save()
            return redirect('bhw_validation')

    context = {'bhw': unvalidate_bhw,
               'form': form}
    return render(request, 'activities/Unvalidated Profile.html', context)


def delete_profile(request, pk):
    delete_bhw = BarangayHealthWorker.objects.get(user_id=pk)
    user_bhw = CustomUser.objects.get(id=pk)

    if request.method == 'POST':

        user_bhw.delete()

        return redirect('bhw_validation')

    context = {'bhw': delete_bhw}
    return render(request, 'activities/Admin Delete Confirmation.html', context)

# ================================== BHW ==================================


@login_required(login_url='login_registration')
def bhw_home(request):
    bhw_logged = BarangayHealthWorker.objects.get(user_id=request.user.id)
    parents = Parent.objects.filter(barangay=bhw_logged.bhw_barangay)
    preschoolers = Preschooler.objects.filter(parent__in=(parents))

    preschooler_normal = []
    preschooler_wasted = []
    preschooler_severly = []
    preschooler_over_obese = []

    for p in preschoolers:
        if p.bmi_tag == 'NORMAL':
            preschooler_normal.append(p)
        elif p.bmi_tag == 'ABOVE NORMAL':
            preschooler_over_obese.append(p)
        elif p.bmi_tag == 'BELOW NORMAL':
            preschooler_wasted.append(p)
        else:
            preschooler_severly.append(p)
    
    normal_count = len(preschooler_normal)
    wasted_count = len(preschooler_wasted)
    severly_count = len(preschooler_severly)
    overobese_count = len(preschooler_over_obese)

    count_list = [normal_count, wasted_count, severly_count, overobese_count, overobese_count]
    data_json = dumps(count_list)

    context = {'bhw' : bhw_logged,
               'normal' : normal_count,
               'wasted' : wasted_count,
               'severly' : severly_count,
               'overobese' : overobese_count,
               'count_data' : data_json}
    return render(request, 'activities/BHW Home.html', context)


def preschooler_dashboard(request):
    preschooler = Preschooler.objects.all()

    context = {'preschoolers': preschooler}
    return render(request, 'activities/BHW Preschooler Dashboard.html', context)


def preschooler_profile(request, pk):
    preschooler = Preschooler.objects.get(id=pk)
    form = UpdatePreschooler(instance=preschooler)

    if request.method == 'POST':
        form = UpdatePreschooler(request.POST, instance=preschooler)
        if form.is_valid():
            form.save()

            return redirect('preschooler_profile', preschooler.id)

    context = {'preschooler' : preschooler,
               'form' : form,}
    return render(request, 'activities/Preschooler Profile.html', context)

# ================================== MODAL UPDATE ==================================


def update_preschooler(request):
    return render(request, 'activities/Preschooler Profile.html')


def immunization_schedule(request):
    return render(request, 'activities/BHW Immunization Schedule.html')
