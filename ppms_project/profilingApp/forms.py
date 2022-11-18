from dataclasses import fields
import imp
from tkinter import Widget
from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django.forms.widgets import PasswordInput
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.core.mail import send_mail

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'autofocus':False})
    """
    A Custom form for creating new users.
    """
    USER_TYPE = [('Choose User Type', 'Choose User Type'),
                 ('BHW', 'Barangay Health Worker'),
                 ('P/G', 'Parent/Guardian')]
                 
    BARANGAYS = [('Select Barangay', 'Select Barangay'),
                 ('Burol', 'Burol'),
                 ('Burol I', 'Burol I'),
                 ('Burol II', 'Burol II'),
                 ('Burol III', 'Burol III'),
                 ('Datu Esmael', 'Datu Esmael'),
                 ('Emmanuel Begado I', 'Emmanuel Begado I'),
                 ('Emmanuel Begado II', 'Emmanuel Begado II'),]
    
    user_type = forms.CharField(label="User Type:", widget=forms.Select(choices=USER_TYPE, attrs={'class' : 'custom-select', 'id' : 'userTypeSelect'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'First Name', 'id' : 'firstname'}))
    middle_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'Middle Name', 'id' : 'middlename'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'Last Name', 'id' : 'lastname'}))
    suffix_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'Suffix', 'id' : 'suffixname'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'name' : 'email', 'type' : 'email', 'id' : 'email', 'placeholder': 'Enter your email address'}))
    password1 = forms.CharField(widget=PasswordInput(attrs={'type' : 'password', 'id' : 'password', 'aria-describeby' : 'passwordHelpBlock', 'placeholder':'Enter your Password', 'data-toggle': 'password'}))
    password2 = forms.CharField(widget=PasswordInput(attrs={'type' : 'password', 'id' : 'cpassword', 'placeholder':'Confirm Your Password','data-toggle': 'password'}))
    barangay = forms.ModelChoiceField(queryset=Barangay.objects.all(), widget=forms.Select(attrs={'class' : 'fstdropdown-select', 'id' : 'brgy'}))
    phone_num = forms.CharField(required=True, widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'Phone Number', 'id' : 'phonenum'}))
    class Meta:
        model = get_user_model()
        fields = ['user_type', 'first_name', 'last_name', 'email', 'phone_num', 'password1', 'password2']
    
    def save(self):
        user = super().save(commit=False)
        user.user_type = self.cleaned_data.get('user_type')
        user.first_name = self.cleaned_data.get('first_name')
        user.middle_name = self.cleaned_data.get('middle_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.suffix_name = self.cleaned_data.get('suffix_name')
        user.email = self.cleaned_data.get('email')
        user.phone_num = self.cleaned_data.get('phone_num')
        user.save()

        if self.cleaned_data.get('user_type') == 'BHW':
            selected_brgy = Barangay.objects.get(brgy_name=self.cleaned_data.get('barangay'))
            bhw = BarangayHealthWorker.objects.create(user=user, bhw_barangay=selected_brgy)
            bhw.save()
        
        if self.cleaned_data.get('user_type') == 'P/G':
            selected_brgy = Barangay.objects.get(brgy_name=self.cleaned_data.get('barangay'))
            png = Parent.objects.create(user=user, barangay=selected_brgy)
            png.save()

        # SEND EMAIL
        # send_mail('Registration Successful',
        #     f"""Congratulations you are now registered. Please double check your registration.\n
        # Here's your username: {user}
        # You are: {user.user_type}
        # Name: {user.first_name} {user.last_name}
        # Email: {user.email}""",
            
        #     'admission.system123@gmail.com',
        #     [f'{user.email}'],
        #     fail_silently=False)

        return user

class Validate_BHW(ModelForm):
    class Meta:
        model = BarangayHealthWorker
        fields = ['is_validated']
        widgets = {'is_validated' : forms.CheckboxInput(attrs={'class' : 'form-check-input', 'type' : 'checkbox'})}
    
    def save(self):
        user = super().save(commit=False)
        user.is_validated = True
        user.save()
        
        return user

class UpdatePreschooler(ModelForm):
    height = forms.FloatField(required=True, max_value=120.0, min_value=45.0, widget=forms.NumberInput(attrs={'class' : 'form-control', 'step': '0.01'}))
    weight = forms.FloatField(required=True, max_value=28.0, min_value=1.0, widget=forms.NumberInput(attrs={'class' : 'form-control', 'step': '0.01'}))
    date_measured = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id' : "date_measured"}))
    health_problem = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control', 'type': 'text', 'id' : 'health_problem'}))

    class Meta:
        model = Preschooler
        fields = ['height', 'weight', 'date_measured', 'health_problem']
