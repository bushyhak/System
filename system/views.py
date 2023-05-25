from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm

# Create your views here.

def home(request):
    return render(request,'system/home.html')

def book(request):
    return render(request,'system/book.html')

def contact(request):
    return render(request, 'system/contact.html')

def about(request):
    return render(request, 'system/about.html')

def login(request):
    return render(request, 'system/login.html')

def register(request):
    return render(request, 'system/register.html')

def user_login(request):
    if request.method =='POST':
        form = LoginForm(request.POST)
        if form.is_valid():

            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authencticated successfully')
                else:
                    return HttpResponse('Disabled account'
                                        )
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
        return render(request, 'system/login.html', {'form':form})



