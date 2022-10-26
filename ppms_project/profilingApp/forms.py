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
    suffix_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'Suffix', 'id' : 'suffixname'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'name' : 'email', 'type' : 'email', 'id' : 'email', 'placeholder': 'Enter your email address'}))
    password1 = forms.CharField(widget=PasswordInput(attrs={'type' : 'password', 'id' : 'password', 'aria-describeby' : 'passwordHelpBlock', 'placeholder':'Enter your Password'}))
    password2 = forms.CharField(widget=PasswordInput(attrs={'type' : 'password', 'id' : 'cpassword', 'placeholder':'Confirm Your Password'}))
    barangay = forms.CharField(label="Barangay:", widget=forms.Select(choices=BARANGAYS, attrs={'class' : 'fstdropdown-select', 'id' : 'brgy'}))
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
            bhw = BarangayHealthWorker.objects.create(user=user)
            bhw.bhw_barangay = self.cleaned_data.get('barangay')
            bhw.save()
        
        if self.cleaned_data.get('user_type') == 'P/G':
            png = Parent.objects.create(user=user)
            png.barangay = self.cleaned_data.get('barangay')
            png.save()

        send_mail('Registration Successful',
            f"""Congratulations you are now registered. Please double check your registration.\n
        Here's your username: {user}
        You are: {user.user_type}
        Name: {user.first_name} {user.last_name}
        Email: {user.email}""",
            
            'admission.system123@gmail.com',
            [f'{user.email}'],
            fail_silently=False)

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

class RegisterPreschooler(ModelForm):
    class Meta:
        model = Preschooler
        fields = ['parent', 'first_name', 'middle_name', 'last_name', 'suffix_name', 'birthday']

        widgets = {'first_name' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Enter your first name'}),
                   'middle_name' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Enter your middle name'}),
                   'last_name' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Enter your last name'}),
                   'suffix_name' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Enter your suffix'}),
                   'birthday' : forms.widgets.DateInput(attrs={'type': 'date', 'class' : 'form-control'})}
    
    # def save(self):
    #     user = super().save(commit=False)
    #     user.parent = self.cleaned_data.get('parent')
    #     user.first_name = self.cleaned_data.get('first_name')
    #     user.middle_name = self.cleaned_data.get('middle_name')
    #     user.last_name = self.cleaned_data.get('last_name')
    #     user.suffix_name = self.cleaned_data.get('suffix_name')
    #     user.birthday = self.cleaned_data.get('birthday')
    #     user.save()

    #     print(user.parent)
    #     return user

        