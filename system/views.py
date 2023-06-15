from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, \
                     UserEditForm, ProfileEditForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Doctor, Profile
from django.contrib import messages
from .forms import ChildForm
from .forms import BookingForm
from random import choice


# Create your views here.
@login_required
def dashboard(request):
    return render(request,
                  'system/dashboard.html',
                  {'section': 'dashboard'})
def home(request):
    return render(request,'system/home.html')

def dashboard(request):
    return render(request, 'system/dashboard.html')
def book(request):
    return render(request,'system/book.html')

def contact(request):
    return render(request, 'system/contact.html')

def about(request):
    return render(request, 'system/about.html')
def logout(request):
    return render(request, 'system/registration/logout.html')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)

            new_user.set_password(
                user_form.cleaned_data['password'])
            
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request,
                          'system/register_done.html',
                          {'new_user': new_user})
                
         
                
    else:
        user_form = UserRegistrationForm()
    return render(request,
                      'system/register.html',
                      {'user_form': user_form})
    
@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile,
                                    data=request.POST,
                                    files=request.FILES)

        if user_form.is_valid and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated '\
                                        'successfully')
        else:
            messages.error(request,'Error updating your profile')

    else:
        user_form = UserEditForm(instance=request.user)   
        profile_form = ProfileEditForm(instance=request.user.profile)     
    return render(request,
                  'system/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})

# adding the child view function
@login_required
def add_child(request):
    if request.method == 'POST':
        form = ChildForm(request.POST)

        if form.is_valid():
            child = form.save(commit=False)
            child.parent = request.user
            child.save()
            return redirect('dashboard')
    else:
            form = ChildForm

    return render(request, 'add_child.html', {'form': form})

@login_required
def booking_view(request):
    if request.method == 'POST':
        form = BookingForm(request.POST, user=request.user)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.parent = request.user

            #Get all available doctors
            doctors = Doctor.objects.all()


            if doctors.exists():
                
                # Randomly select a doctor from the available doctors

                random_doctor = choice(doctors)
                appointment.doctor = random_doctor
                appointment.status = 'Confirmed'
                appointment.save()

                # Update the doctor's appoitment

                random_doctor.appointments.add(appointment)
                appointment.save()

                return redirect('dashboard')
            
            else: 
                return HttpResponse('No Doctors availabe')
            
        
    else:
        form = BookingForm(user=request.user)

    context = {'form': form}
    return render(request, 'booking.html', context)



    










# def user_login(request):
#     if request.method =='POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():

#             cd = form.cleaned_data
#             user = authenticate(request,
#                                 username=cd['username'],
#                                 password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse('Authencticated successfully')
#                 else:
#                     return HttpResponse('Disabled account'
#                                         )
#             else:
#                 return HttpResponse('Invalid login')
#     else:
#         form = LoginForm()
#         return render(request, 'system/login.html', {'form':form})



