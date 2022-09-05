from dataclasses import fields
from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django.forms.widgets import PasswordInput
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
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

        return user