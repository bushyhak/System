from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request,'system/home.html')

def appointment(request):
    return render(request,'system/appointment.html')

def contact(request):
    return render(request, 'system/contact.html')

def schedule(request):
    return render(request, 'system/about.html')
def login(request):
    return render(request, 'system/login.html')


