from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .helpers import send_booking_confirmation_email, vaccine_in_child_appointments
from .models import Doctor, Appointment, Vaccines, Child, Feedback
from .forms import (
    ChildUpdateForm,
    FeedbackForm,
    UserRegistrationForm,
    UserEditForm,
    ProfileEditForm,
    ChildForm,
    BookingForm,
    CancelForm,
    RescheduleForm,
)


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
    all_my_appointments = Appointment.objects.filter(child__parent=request.user)

    # only get upcoming appointments [in the future & not cancelled]
    appointments = all_my_appointments.filter(cancelled=False)  # completed=False
    appointments = [ap for ap in appointments if not ap.has_passed()]

    vaccine_schedules = []
    vaccines = Vaccines.objects.all()
    children = Child.objects.filter(parent=request.user)
    for child in children:
        age = child.age_in_weeks
        next_vaccines = vaccines.filter(
            weeks_minimum_age__lte=age, weeks_maximum_age__gte=age
        )
        for vaccine in next_vaccines:
            if not vaccine_in_child_appointments(vaccine, child):
                vaccine_schedules.append((child, vaccine))

    context = {
        "appointments": appointments,
        "vaccine_schedules": vaccine_schedules,
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
            messages.success(request, "Child added successfully")
            return redirect("dashboard_child_info")
        else:
            messages.error(request, "Failed to add child")
    else:
        form = ChildForm()
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


@login_required
def update_child(request, child_id):
    """Update records of an existing child"""
    child = get_object_or_404(Child, id=child_id, parent=request.user)
    child_detail_url = reverse("child_detail", kwargs={"child_id": child_id})

    if request.method == "POST":
        form = ChildUpdateForm(request.POST, instance=child)
        if form.is_valid():
            form.save()
            messages.success(request, "Child updated successfully.")
            return redirect(child_detail_url, permanent=True)
        else:
            messages.error(request, "Failed to update child")
    else:
        form = ChildUpdateForm(instance=child)
    breadcrumb = [
        {"label": "Child Info", "url": reverse("dashboard_child_info")},
        {"label": "Child Detail", "url": child_detail_url},
        {"label": "Update Child", "url": None},
    ]
    context = {
        "form": form,
        "breadcrumb": breadcrumb,
    }
    return render(request, "system/child/update.html", context)


@login_required
def delete_child(request, child_id):
    """Delete an existing child"""
    child = get_object_or_404(Child, id=child_id, parent=request.user)

    if request.method == "POST":
        child.delete()
        messages.success(request, "Child deleted successfully")
        return redirect("dashboard_child_info", permanent=True)

    breadcrumb = [
        {"label": "Child Info", "url": reverse("dashboard_child_info")},
        {
            "label": "Child Detail",
            "url": reverse("child_detail", kwargs={"child_id": child_id}),
        },
        {"label": "Delete Child", "url": None},
    ]

    context = {"breadcrumb": breadcrumb, "child": child}
    return render(request, "system/child/delete.html", context)


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

    class Filters:
        child = None
        status = None

        @property
        def list(self):
            items = []
            if isinstance(self.child, str):
                items.append(self.child)

            if self.status and isinstance(self.status, str):
                items.append(self.status)

            return items

    appointments = Appointment.objects.filter(child__parent=request.user)
    if not request.GET:  # by default, don't show cancelled appointments
        appointments = appointments.filter(cancelled=False)

    children = Child.objects.filter(parent=request.user)

    if child := request.GET.get("child"):
        fname, lname = child.split(" ")
        appointments = appointments.filter(
            child__first_name=fname.strip(),
            child__last_name=lname.strip(),
        )
        Filters.child = child
    if status := request.GET.get("status"):
        if status == "Cancelled":
            appointments = appointments.filter(cancelled=True)
            Filters.status = status
        elif status == "Complete":
            appointments = appointments.filter(completed=True, cancelled=False)
            Filters.status = status
        elif status == "Pending":
            appointments = appointments.filter(completed=False, cancelled=False)
            Filters.status = status

    # if completed := request.GET.get("completed"):
    #     appointments = appointments.filter(completed=completed)
    #     Filters.completed = completed
    # if cancelled := request.GET.get("cancelled"):
    #     appointments = appointments.filter(cancelled=cancelled)
    #     Filters.cancelled = cancelled

    context = {"appointments": appointments, "children": children, "filters": Filters}
    return render(request, "system/appointments/list.html", context)


@login_required
def appointment_detail(request, id):
    """Get the details of a single appointment using the id"""
    appointment = Appointment.objects.get(id=id)
    feedbacks = Feedback.objects.filter(appointment=appointment)

    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.parent = request.user
            feedback.appointment = appointment
            feedback.save()
            messages.success(request, "Feedback added successfully")
        else:
            messages.error(request, "Failed to add feedback")
    else:
        form = FeedbackForm()

    breadcrumb = [
        {"label": "Appointments", "url": reverse("appointments")},
        {"label": "Appointment Detail", "url": None},
    ]
    context = {
        "appointment": appointment,
        "breadcrumb": breadcrumb,
        "feedbacks": feedbacks,
        "form": form,
    }
    return render(request, "system/appointments/detail.html", context)


@login_required
def book_appointment(request):
    """Book a new appointment"""
    if request.method == "POST":
        form = BookingForm(request.POST, user=request.user, request=request)
        if form.is_valid():
            appointment = form.save(commit=False)
            doctor = Doctor.get_available_doctor(appointment.date, appointment.time)

            if doctor:
                appointment.doctor = doctor
                appointment.save()

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

            if new_date == appointment.date and new_time == appointment.time:
                form.add_error("time", "Please select a different time than before")

            # Update the appointment's date and time
            if not form.errors:
                appointment.date = new_date
                appointment.time = new_time
                appointment.save()

                messages.success(request, "Appointment rescheduled successfully.")
                return redirect("appointments", permanent=True)
            else:
                messages.error(request, "Failed to reschedule appointment")
        else:
            messages.error(request, "Failed to reschedule appointment")
    else:
        form = RescheduleForm(instance=appointment)
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
    appointment = get_object_or_404(Appointment, id=id, child__parent=request.user)

    if request.method == "POST":
        form = CancelForm(request.POST, instance=appointment)
        if form.is_valid():
            appointment.cancelled = True
            appointment.save()
            messages.success(request, "Appointment cancelled successfully!")
            return redirect("appointments", permanent=True)
        else:
            messages.error(request, "Failed to cancel appointment")
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
