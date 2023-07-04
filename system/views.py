from datetime import date, time
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.urls import reverse
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Doctor, Profile, Appointment, Vaccines, User
from .forms import ChildForm, BookingForm, CancelForm
from random import choice
from .forms import RescheduleForm
from django.contrib import messages
from .models import Child
from django.core.mail import send_mail
from django.template.loader import render_to_string


def home(request):
    return render(request, "system/home.html")


def contact(request):
    return render(request, "system/contact.html")


def about(request):
    return render(request, "system/about.html")


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


@login_required
def dashboard(request):
    return render(request, "system/dashboard/base.html")


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

    return render(request, "system/dashboard/add_child.html", {"form": form})


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


@login_required
def settings(request):
    return render(request, "system/dashboard/settings.html")


@login_required
def report(request):
    return render(request, "system/dashboard/report.html")


@login_required
def book(request):
    return render(request, "system/book.html")


@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)

        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )

        if user_form.is_valid() and profile_form.is_valid():
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
def booking_view(request):
    if request.method == "POST":
        form = BookingForm(request.POST, user=request.user, request=request)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.child = request.user

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
