from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CustomUserCreationForm
# Create your views here.

def index(request):
    return HttpResponse('Hello World')

def registration(request):
    form = CustomUserCreationForm()
    print("Working Form")

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        print("Form Submitted")
        if form.is_valid():
            form.save()
            return redirect('registration')
    context = {'form' : form}
    return render(request, 'activities/index.html', context)