from itertools import count
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import *
from .models import *
from datetime import datetime, timedelta
from json import dumps
# Create your views here.


def index(request):
    return HttpResponse('Hello World')


@unauthenticated_user
def login_registration(request):
    print(Preschooler.objects.all())
    print(Preschooler.gte_60_objects.all())
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
            current_date =  datetime.now()
            format_date =  current_date.strftime("%Y/%m/%d, %H:%M:%S")
            user_email = request.POST.get('email')
            password = request.POST.get('password')

            user = authenticate(request, email=user_email, password=password)
            if user is not None and user.user_type == 'P/G':
                login(request, user)
                Log.objects.create(log_action = 'Logged IN', logged_userid  = user.id, datetime_log = format_date
                )
                return redirect('parent_home')
                
            elif user is not None and user.user_type == 'BHW':
                bhw_validation_status = BarangayHealthWorker.objects.get(
                    user=user)
                if bhw_validation_status.is_validated:
                    login(request, user)
                    Log.objects.create(log_action = 'logged in', logged_userid  = user.id, datetime_log = format_date
                )
                    return redirect('bhw_home')
                else:
                    # Error message pop-up
                    messages.warning(
                        request, 'Please wait for the validation.')
            elif user is not None and user.user_type == 'Admin':
                login(request, user)
                Log.objects.create(log_action = 'logged in', logged_userid  = user.id, datetime_log = format_date
                )
                return redirect('admin_home')
            else:
                messages.error(request, 'Login Failed')

    context = {'form': form}
    return render(request, 'activities/login_registration.html', context)


def logout_user(request):
    user= request.user
    current_date =  datetime.now()
    format_date =  current_date.strftime("%Y/%m/%d, %H:%M:%S")
    Log.objects.create(log_action = 'Logged Out', logged_userid  = user.id, datetime_log = format_date
                )
    logout(request)
    return redirect('login_registration')

# ================================== PARENTS/GUARDIANS ==================================

@login_required(login_url='login_registration')
def parent_home(request):
    if request.user.is_authenticated and request.user.user_type == 'P/G':
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

        if len(preschooler) <= 2:
            numberOfColumns = 6
            bootstrapColWidth = int(12 / numberOfColumns)
            chunks = [preschooler[i:i+bootstrapColWidth] for i in range(0,len(preschooler),bootstrapColWidth)]
            context = {
                'chunks': chunks,
                'numberOfColumns': numberOfColumns,
                'bootstrapColWidth' : bootstrapColWidth
            }
            return render(request, 'activities/Parent Home.html', context)
        else:
            numberOfColumns = 4
            bootstrapColWidth = int(12 / numberOfColumns)
            chunks = [preschooler[i:i+bootstrapColWidth] for i in range(0,len(preschooler),bootstrapColWidth)]
            context = {
                'chunks': chunks,
                'numberOfColumns': numberOfColumns,
                'bootstrapColWidth' : bootstrapColWidth
            }
            return render(request, 'activities/Parent Home.html', context)
    
    elif request.user.is_authenticated and request.user.user_type == 'BHW':
        return redirect('bhw_home')
    elif request.user.is_authenticated and request.user.user_type == 'Admin':
        return redirect('admin_home')

def parent_preschooler(request, pk):
    if request.user.is_authenticated and request.user.user_type == 'P/G':
        preschooler = Preschooler.objects.get(id=pk)

        context = {'preschooler' : preschooler}
        return render(request, 'activities/Parent - Preschooler Profile.html', context)
    elif request.user.is_authenticated and request.user.user_type == 'BHW':
        return redirect('bhw_home')
    elif request.user.is_authenticated and request.user.user_type == 'Admin':
        return redirect('admin_home')
        

# ================================== ADMIN ==================================

@login_required(login_url='login_registration')
def admin_home(request):
    if request.user.is_authenticated and request.user.user_type == 'Admin':
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
        
    elif request.user.is_authenticated and request.user.user_type == 'BHW':
        return redirect('bhw_home')
    elif request.user.is_authenticated and request.user.user_type == 'P/G':
        return redirect('parent_home')


def bhw_validation(request):
    if request.user.is_authenticated and request.user.user_type == 'Admin':
        bhw = BarangayHealthWorker.objects.filter(is_validated=False)

        parent = Parent.objects.all()
        invalidated_status = BarangayHealthWorker.objects.filter(
            is_validated=False).count()

        context = {'bhws': bhw, 
                'invalidated_count': invalidated_status,
                'parents' : parent,}

        return render(request, 'activities/Admin - Validation.html', context)
    
    elif request.user.is_authenticated and request.user.user_type == 'BHW':
        return redirect('bhw_home')
    elif request.user.is_authenticated and request.user.user_type == 'P/G':
        return redirect('parent_home')

def set_pass(request, pk):
    if request.user.is_authenticated and request.user.user_type == 'Admin':
        user = CustomUser.objects.get(id=pk)
        form = SetPasswordForm(user)
        
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Password changed.')
            else:
                messages.error(request, 'New Password did not match. Please fill up the form correctly!')

        print(user)
        context = {'form' : form, 'user' :user}

        return render(request, 'activities/Admin - Set Password.html', context)

    elif request.user.is_authenticated and request.user.user_type == 'BHW':
        return redirect('bhw_home')
    elif request.user.is_authenticated and request.user.user_type == 'P/G':
        return redirect('parent_home')

def admin_preschoolers(request):
    if request.user.is_authenticated and request.user.user_type == 'Admin':
        invalidated_status = BarangayHealthWorker.objects.filter(
            is_validated=False).count()

        barangays = Barangay.objects.all()

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
                'barangays' : barangays,
                'count_data' : data_json}

        return render(request, 'activities/Admin - Preschooler.html', context)

    elif request.user.is_authenticated and request.user.user_type == 'BHW':
        return redirect('bhw_home')
    elif request.user.is_authenticated and request.user.user_type == 'P/G':
        return redirect('parent_home')

def admin_preschoolers_barangay(request, brgy):
    if request.user.is_authenticated and request.user.user_type == 'Admin':
        invalidated_status = BarangayHealthWorker.objects.filter(
            is_validated=False).count()

        parents = Parent.objects.filter(barangay=brgy)
        preschoolers = Preschooler.objects.filter(parent__in=(parents))
        
        barangay = Barangay.objects.get(id=brgy)
        barangays = Barangay.objects.all()

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
                'brgy' : barangay,
                'normal' : normal_count,
                'wasted' : wasted_count,
                'severly' : severly_count,
                'overobese' : overobese_count,
                'barangays' : barangays,
                'count_data' : data_json
                }

        return render(request, 'activities/Admin - Preschooler_barangay.html', context)
    
    elif request.user.is_authenticated and request.user.user_type == 'BHW':
        return redirect('bhw_home')
    elif request.user.is_authenticated and request.user.user_type == 'P/G':
        return redirect('parent_home')

def unvalidated_profile(request, pk):
    if request.user.is_authenticated and request.user.user_type == 'Admin':
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

    elif request.user.is_authenticated and request.user.user_type == 'BHW':
        return redirect('bhw_home')
    elif request.user.is_authenticated and request.user.user_type == 'P/G':
        return redirect('parent_home')


def delete_profile(request, pk):
    if request.user.is_authenticated and request.user.user_type == 'Admin':
        delete_bhw = BarangayHealthWorker.objects.get(user_id=pk)
        user_bhw = CustomUser.objects.get(id=pk)

        if request.method == 'POST':

            user_bhw.delete()

            return redirect('bhw_validation')

        context = {'bhw': delete_bhw}
        return render(request, 'activities/Admin Delete Confirmation.html', context)
    
    elif request.user.is_authenticated and request.user.user_type == 'BHW':
        return redirect('bhw_home')
    elif request.user.is_authenticated and request.user.user_type == 'P/G':
        return redirect('parent_home')


def admin_barangay(request):
    if request.user.is_authenticated and request.user.user_type == 'Admin':
        invalidated_status = BarangayHealthWorker.objects.filter(
            is_validated=False).count()
        barangays = Barangay.objects.all()

        form = AddBarangay()
        if request.method == 'POST':
            form = AddBarangay(request.POST)
            
            if form.is_valid():
                form.save()
                
                return redirect('admin_barangay')

        context = {'barangays' : barangays,
                   'invalidated_count' : invalidated_status,
                   'form' : form}
    
        return render(request, 'activities/Admin - barangay.html', context)

def admin_userAccounts(request):
    if request.user.is_authenticated and request.user.user_type == 'Admin':
        all_bhw = BarangayHealthWorker.objects.all()
        all_parents = Parent.objects.all()

        invalidated_status = BarangayHealthWorker.objects.filter(
            is_validated=False).count()

        context = {'bhws': all_bhw,
                    'invalidated_count': invalidated_status,
                   'parents' : all_parents}
    
        return render(request, 'activities/Admin - User accounts.html', context)

# ================================== BHW ==================================


@login_required(login_url='login_registration')
def bhw_home(request):
    if request.user.is_authenticated and request.user.user_type == 'BHW':
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
    
    elif request.user.is_authenticated and request.user.user_type == 'Admin':
        return redirect('admin_home')
    elif request.user.is_authenticated and request.user.user_type == 'P/G':
        return redirect('parent_home')


def preschooler_dashboard(request):
    if request.user.is_authenticated and request.user.user_type == 'BHW':
        bhw_logged = BarangayHealthWorker.objects.get(user_id=request.user.id)
        parents = Parent.objects.filter(barangay=bhw_logged.bhw_barangay)
        preschooler = Preschooler.objects.filter(parent__in=(parents))

        context = {'preschoolers': preschooler}
        return render(request, 'activities/BHW Preschooler Dashboard.html', context)

    elif request.user.is_authenticated and request.user.user_type == 'Admin':
        return redirect('admin_home')
    elif request.user.is_authenticated and request.user.user_type == 'P/G':
        return redirect('parent_home')

def preschooler_profile(request, pk):
    if request.user.is_authenticated and request.user.user_type == 'BHW':
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

    elif request.user.is_authenticated and request.user.user_type == 'Admin':
        return redirect('admin_home')
    elif request.user.is_authenticated and request.user.user_type == 'P/G':
        return redirect('parent_home')

# ================================== MODAL UPDATE ==================================


def update_preschooler(request):
    return render(request, 'activities/Preschooler Profile.html')


def immunization_schedule(request, pk):
    preschooler = Preschooler.objects.get(id=pk)
    vaccines = Vaccine.objects.filter(vax_preschooler=preschooler)
    vax_list = vaccines.values_list('vax_name', flat=True)
    dose_list = vaccines.values_list('vax_dose', flat=True)

    if request.method == 'POST':
        preschooler_obj = preschooler
        vaxname = request.POST.get('vax_name')
        dose = request.POST.get('dose')
        vaxdate = request.POST.get('immune_date')
        vaxremark = request.POST.get('remarks')

        vax_create = Vaccine.objects.update_or_create(vax_preschooler=preschooler_obj,
                                            vax_name=vaxname,
                                            defaults={'vax_dose' : dose,
                                                      'vax_date' : vaxdate,
                                                      'vax_remarks' : vaxremark})
        
        return redirect('immunization_schedule', pk=preschooler.id)
        
    context = {'vaccines' : vaccines,
               'vax_list' : vax_list,
               'dose_list' : dose_list,
               'preschooler':preschooler}


    return render(request, 'activities/BHW Immunization Status.html', context)
