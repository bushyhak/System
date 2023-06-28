from datetime import date, time
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from system import report
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Doctor, Profile, Appointment, Vaccines
from .forms import ChildForm, BookingForm, CancelForm
from random import choice
from .forms import RescheduleForm
from django.contrib import messages
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.utils import quote
from .models import Child
from django.core.mail import send_mail, EmailMessage
from bookingsys.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string


# Create your views here.
@login_required
def dashboard(request):
    return render(request, "system/dashboard.html", {"section": "dashboard"})


def home(request):
    return render(request, "system/home.html")


def dashboard(request):
    return render(request, "system/dashboard.html")


def book(request):
    return render(request, "system/book.html")


def contact(request):
    return render(request, "system/contact.html")


def about(request):
    return render(request, "system/about.html")


def logout(request):
    return render(request, "system/registration/logout.html")


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # new_user = user_form.save(commit=False)
            new_user = user_form.save()

            # new_user.set_password(
            #     user_form.cleaned_data['password'])

            # new_user.save()

            # Profile.objects.create(user=new_user)
            return render(request, "system/register_done.html", {"new_user": new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, "system/register.html", {"user_form": user_form})


@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)

        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )

        if user_form.is_valid and profile_form.is_valid():
            user_form.save()
            profile_form.save()

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(
        request,
        "system/edit.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


@login_required
def add_child(request):
    if request.method == "POST":
        form = ChildForm(request.POST)

        if form.is_valid():
            child = form.save(commit=False)
            child.parent = request.user
            child.save()
            return redirect("dashboard")
    else:
        form = ChildForm

    return render(request, "add_child.html", {"form": form})


@login_required
def child_detail(request, child_id):
    child = get_object_or_404(Child, id=child_id, parent=request.user)
    return render(request, "child_detail.html", {"child": child})


@login_required
def booking_view(request):
    if request.method == "POST":
        form = BookingForm(request.POST, user=request.user, request=request)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.parent = request.user

            doctors = Doctor.objects.all()

            if doctors.exists():
                random_doctor = choice(doctors)
                appointment.doctor = random_doctor
                appointment.status = "Pending"
                appointment.save()

                random_doctor.appointments.add(appointment)
                appointment.save()

                return redirect("dashboard")

            else:
                return HttpResponse("No Doctors availabe")

    else:
        form = BookingForm(user=request.user, request=request)

    context = {"form": form}
    return render(request, "booking.html", context)


@login_required
def reschedule_view(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, parent=request.user)

    if request.method == "POST":
        form = RescheduleForm(request.POST)
        if form.is_valid():
            new_date = form.cleaned_data["date"]
            new_time = form.cleaned_data["time"]

            if new_date < date.today():
                form.add_error(
                    "date", "Invalid date. Please select a date in the future"
                )
            elif new_date == appointment.date and new_time == appointment.time:
                form.add_error("time", "Please select a different time")

            # Update the appointment's date and time
            if not form.errors:
                appointment.date = new_date
                appointment.time = new_time
                appointment.save()

                # # Create an admin log entry for the rescheduled appointment
                # log_entry = LogEntry.objects.log_action(
                #     user_id=request.user.id,
                #     content_type_id=ContentType.objects.get_for_model(appointment).pk,
                #     object_id=appointment.id,
                #     object_repr=str(appointment),
                #     action_flag=CHANGE,
                #     change_message="Appointment rescheduled by user",
                # )
                # log_entry.save()

                messages.success(request, "Appointment rescheduled successfully.")

                return redirect("dashboard")
    else:
        form = RescheduleForm()

    context = {"form": form}
    return render(request, "reschedule.html", context)


@login_required
def cancel_appointment(request, appointment_id):
    appointment = Appointment.objects.get(pk=appointment_id)

    if request.method == "POST":
        form = CancelForm(request.POST, instance=appointment)
        if form.is_valid():
            appointment.delete()
            return redirect("dashboard")
    else:
        form = CancelForm(instance=appointment)

    return render(
        request, "cancel_appointment.html", {"form": form, "appointment": appointment}
    )


def send_booking_confirmation_email(appointment):
    parent_email = appointment.parent.email
    subject = "Booking Confirmation"
    message = render_to_string("confirm_booking.html", {"appointment": appointment})
    send_mail(subject, message, "your_email@example.com", [parent_email])


# def cancel_view(request, appointment_id):
#     appointment = get_object_or_404(Appointment, id=appointment_id, parent=request.user)

#     if request.method == 'POST':
#         appointment.delete()
#         return redirect('dashboard')

#     form = CancelForm()
#     context = {'form': form}
#     return render(request, 'cancel.html', context)
