from dataclasses import fields
import imp
from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django.forms.widgets import PasswordInput
from django.contrib.auth.forms import UserCreationForm
from .models import BarangayHealthWorker
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
    
    user_type = forms.CharField(label="User Type:", widget=forms.Select(choices=USER_TYPE, attrs={'class' : 'custom-select', 'id' : 'userTypeSelect'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'First Name', 'id' : 'firstname'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'Last Name', 'id' : 'lastname'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'name' : 'email', 'type' : 'email', 'id' : 'email', 'placeholder': 'Enter your email address'}))
    password1 = forms.CharField(widget=PasswordInput(attrs={'type' : 'password', 'id' : 'password', 'aria-describeby' : 'passwordHelpBlock', 'placeholder':'Enter your Password'}))
    password2 = forms.CharField(widget=PasswordInput(attrs={'type' : 'password', 'id' : 'cpassword', 'placeholder':'Confirm Your Password'}))
    
    class Meta:
        model = get_user_model()
        fields = ['user_type', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
    def save(self):
        user = super().save(commit=False)
        user.user_type = self.cleaned_data.get('user_type')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.save()

        if self.cleaned_data.get('user_type') == 'BHW':
            bhw = BarangayHealthWorker.objects.create(user=user)
            bhw.save()

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