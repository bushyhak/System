from datetime import date, time
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.urls import reverse
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Doctor, Appointment, Vaccines, User
from .forms import ChildForm, BookingForm, CancelForm
from random import choice
from .forms import RescheduleForm
from django.contrib import messages
from .models import Child
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings as django_settings


##################################### Landing Site #####################################
def home(request):
    return render(request, "system/home.html")


def contact(request):
    return render(request, "system/contact.html")


def about(request):
    return render(request, "system/about.html")


##################################### Auth #####################################
def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save()
            messages.success(
                request,
                f"'{new_user.username}', your account has been successfully created. Now you can Log in",  # noqa: E501
            )
            return redirect("login", permanent=True)
    else:
        user_form = UserRegistrationForm()
    return render(request, "system/auth/register.html", {"user_form": user_form})


##################################### Dashboard #####################################
@login_required
def dashboard(request):
    appointments = Appointment.objects.filter(child__parent=request.user)
    context = {
        "appointments": appointments,
    }
    return render(request, "system/dashboard/base.html", context)


##################### Profile
@login_required
def profile(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile saved successfully")
        else:
            messages.error(request, "Failed to save Profile")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, "system/dashboard/profile.html", context)


##################### Children Info
@login_required
def child_info(request):
    children = Child.objects.filter(parent=request.user)
    context = {"children": children}
    return render(request, "system/dashboard/child-info.html", context)


@login_required
def add_child(request):
    if request.method == "POST":
        form = ChildForm(request.POST)

        if form.is_valid():
            child = form.save(commit=False)
            child.parent = request.user
            child.save()
            return redirect("dashboard_child_info")
    else:
        form = ChildForm
    breadcrumb = [
        {"label": "Dashboard", "url": reverse("dashboard")},
        {"label": "Child Info", "url": reverse("dashboard_child_info")},
        {"label": "Add Child", "url": None},
    ]
    context = {
        "form": form,
        "breadcrumb": breadcrumb,
    }
    return render(request, "system/dashboard/add_child.html", context)


@login_required
def child_detail(request, child_id):
    child = get_object_or_404(Child, id=child_id, parent=request.user)
    breadcrumb = [
        {"label": "Child Info", "url": reverse("dashboard_child_info")},
        {"label": "Child Detail", "url": None},
    ]
    context = {
        "child": child,
        "breadcrumb": breadcrumb,
    }
    return render(request, "system/dashboard/child_detail.html", context)


##################### Settings
@login_required
def settings(request):
    return render(request, "system/dashboard/settings.html")


##################### Report
@login_required
def report(request):
    return render(request, "system/dashboard/report.html")


##################### Appointments
@login_required
def appointments(request):
    """List all appointments"""
    appointments = Appointment.objects.filter(child__parent=request.user)
    context = {
        "appointments": appointments,
    }
    return render(request, "system/appointments/list.html", context)


@login_required
def appointment_detail(request, id):
    """Get the details of a single appointment using the id"""
    appointment = Appointment.objects.get(id=id)

    breadcrumb = [
        {"label": "Appointments", "url": reverse("appointments")},
        {"label": "Appointment Detail", "url": None},
    ]
    context = {
        "appointment": appointment,
        "breadcrumb": breadcrumb,
    }
    return render(request, "system/appointments/detail.html", context)


def send_booking_confirmation_email(appointment):
    """Helper function to send an appointment booking confirmation"""
    subject = "Appointment Booking Confirmation"
    parent_email = appointment.child.parent.email
    context = {"appointment": appointment}
    html_message = render_to_string("system/appointments/confirm_booking.html", context)
    plain_message = strip_tags(html_message)
    from_email = django_settings.DEFAULT_FROM_EMAIL
    send_mail(
        subject,
        plain_message,
        from_email,
        recipient_list=[parent_email],
        html_message=html_message,
    )


@login_required
def book_appointment(request):
    """Book a new appointment"""
    if request.method == "POST":
        form = BookingForm(request.POST, user=request.user, request=request)
        if form.is_valid():
            appointment = form.save(commit=False)
            # appointment.child = request.user

            doctors = Doctor.objects.filter(available=True)  # get available doctors

            if doctors.exists():
                doctor = choice(doctors)  # choose random doctor
                appointment.doctor = doctor
                appointment.save()
                doctor.available = False
                doctor.save()
                # random_doctor.appointments.add(appointment)
                # appointment.save()
                send_booking_confirmation_email(appointment)
                messages.success(request, "Appointment booked successfully!")
                return redirect("appointments")
            else:
                messages.error(request, "No Doctors available at the moment.")
        else:
            messages.error(request, "Failed to book appointment!")
    else:
        form = BookingForm(user=request.user, request=request)

    breadcrumb = [
        {"label": "Appointments", "url": reverse("appointments")},
        {"label": "New Appointment", "url": None},
    ]
    context = {
        "form": form,
        "breadcrumb": breadcrumb,
    }
    return render(request, "system/appointments/new.html", context)


@login_required
def reschedule_appointment(request, id):
    """Reschedule an existing appointment"""
    appointment = get_object_or_404(Appointment, id=id)

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

                messages.success(request, "Appointment rescheduled successfully.")
                return redirect("appointments")
            else:
                print(form.non_field_errors)
                messages.error(request, "Failed to reschedule appointment")
    else:
        form = RescheduleForm()
    breadcrumb = [
        {"label": "Appointments", "url": reverse("appointments")},
        {
            "label": "Appointment Detail",
            "url": reverse("appointment_detail", kwargs={"id": id}),
        },
        {"label": "Reschedule", "url": None},
    ]
    context = {
        "form": form,
        "breadcrumb": breadcrumb,
    }
    return render(request, "system/appointments/reschedule.html", context)


@login_required
def cancel_appointment(request, id):
    """Cancel an existing appointment"""
    appointment = Appointment.objects.get(id=id)

    if request.method == "POST":
        form = CancelForm(request.POST, instance=appointment)
        if form.is_valid():
            # appointment.delete() appointment.cancel = True, save()
            return redirect("appointments")
    else:
        form = CancelForm(instance=appointment)
    breadcrumb = [
        {"label": "Appointments", "url": reverse("appointments")},
        {
            "label": "Appointment Detail",
            "url": reverse("appointment_detail", kwargs={"id": id}),
        },
        {"label": "Cancel", "url": None},
    ]
    context = {
        "form": form,
        "appointment": appointment,
        "breadcrumb": breadcrumb,
    }
    return render(request, "system/appointments/cancel.html", context)
