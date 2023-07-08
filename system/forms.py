from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import Select, DateInput
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

from .models import Feedback, Profile, Child, Appointment, Vaccines
from system.helpers import (
    combine_date_time,
    date_less_than_today,
    datetime_less_than_now,
    get_local_now,
)


class CustomModelForm(forms.ModelForm):
    """Extend the django ModelForm, adding "form-control" css class and a placeholder"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name.lower().find("date") >= 0:
                field.widget.input_type = "date"
            if field_name.lower().find("phone") >= 0:
                field.widget.input_type = "tel"

            if isinstance(field.widget, Select):
                self.add_class(field, "form-select")
            else:
                self.add_class(field, "form-control")

            if not field.widget.attrs.get("placeholder"):
                txt = field.label.lower() if field.label else "data"
                field.widget.attrs["placeholder"] = "Enter %s..." % txt

    def add_class(self, field, css_class):
        if field.widget.attrs.get("class"):
            field.widget.attrs["class"] += f" {css_class}"
        else:
            field.widget.attrs["class"] = css_class

    def add_error(self, field: str | None, error: ValidationError | str) -> None:
        self.add_class(self.fields.get(field), "is-invalid")
        return super().add_error(field, error)


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

    def clean_email(self):
        data = self.cleaned_data["email"]
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("Email already in use.")
        return data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].help_text = ""


class UserEditForm(CustomModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    def clean_email(self):
        data = self.cleaned_data["email"]
        qs = User.objects.exclude(id=self.instance.id).filter(email=data)
        if qs.exists():
            raise forms.ValidationError("Email already in use")
        return data


class ProfileEditForm(CustomModelForm):
    class Meta:
        model = Profile
        fields = ["date_of_birth", "phone_number"]

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get("date_of_birth")

        if date_of_birth:
            if date_of_birth > get_local_now().date():
                raise forms.ValidationError("Date of birth cannot be in the future")

        return date_of_birth

    def clean_phone_number(self):
        phone_number: str = self.cleaned_data.get("phone_number")
        if not (
            phone_number.startswith("+254")
            or phone_number.startswith("07")
            or phone_number.startswith("01")
        ):
            raise forms.ValidationError("Phone number must start with +254, 07, or 01.")
        if not phone_number[1:].isdigit():
            raise forms.ValidationError(
                "Phone number must contain only + symbol and digits"
            )
        if len(phone_number) != 10 and len(phone_number) != 13:
            if phone_number.startswith("+254"):
                raise forms.ValidationError(
                    "Phone number must be 9 digits after '+254'"
                )
            if phone_number.startswith("07"):
                raise forms.ValidationError("Phone number must be 8 digits after '07'")
            if phone_number.startswith("01"):
                raise forms.ValidationError("Phone number must be 8 digits after '01'")
        return phone_number


class ChildForm(CustomModelForm):
    class Meta:
        model = Child
        fields = ["first_name", "last_name", "gender", "date_of_birth"]
        widgets = {"date_of_birth": DateInput(attrs={"type": "date"})}

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get("date_of_birth")
        if not date_of_birth:  # prevents errors below if date_of_birth is None
            return date_of_birth

        if date_of_birth > get_local_now().date():
            raise forms.ValidationError("Child's date of birth cannot be in the future")

        age_in_months = (get_local_now().date() - date_of_birth).days // 30

        if age_in_months > 18:
            raise forms.ValidationError("Child must be 18 months or below.")

        return date_of_birth


# Custom widget to display hour intervals for time field
class HourIntervalSelectWidget(Select):
    intervals = [
        ("08:00", "08:00 AM"),
        ("09:00", "09:00 AM"),
        ("10:00", "10:00 AM"),
        ("11:00", "11:00 AM"),
        ("12:00", "12:00 PM"),
        ("13:00", "1:00 PM"),
        ("14:00", "2:00 PM"),
        ("15:00", "3:00 PM"),
        ("16:00", "4:00 PM"),
    ]

    def __init__(self, attrs=None, choices=None):
        if choices is None:
            choices = self.intervals
        super().__init__(attrs=attrs, choices=choices)


class BookingForm(CustomModelForm):
    """Form for booking appointments"""

    child = forms.ModelChoiceField(queryset=Child.objects.all())
    vaccine = forms.ModelChoiceField(queryset=Vaccines.objects.all())

    class Meta:
        model = Appointment
        fields = ["child", "date", "time", "vaccine"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "time": HourIntervalSelectWidget(attrs={"type": "time"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        self.request = kwargs.pop("request")
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields["child"].queryset = Child.objects.filter(parent=user)
        # self.fields["vaccine"].queryset = Vaccines.objects.filter()

    def clean_date(self):
        selected_date = self.cleaned_data.get("date")
        if selected_date:
            # Validate that the selected date is not in the past
            if date_less_than_today(selected_date):
                raise forms.ValidationError(
                    "Invalid date. Please select a date in the future"
                )

            # Check if the selected date is fully booked
            appointment_count = Appointment.objects.filter(date=selected_date).count()
            if appointment_count >= 50:
                raise forms.ValidationError(
                    "This date is fully booked. Please select another date."
                )
        return selected_date

    def clean_time(self):
        selected_time = self.cleaned_data.get("time")
        allowed_times = [interval[0] for interval in HourIntervalSelectWidget.intervals]
        if selected_time.strftime("%H:%M") not in allowed_times:
            raise forms.ValidationError("Please select a valid time.")

        if selected_date := self.cleaned_data.get("date"):
            date_time = combine_date_time(selected_date, selected_time)
            if datetime_less_than_now(date_time):
                raise forms.ValidationError(
                    "Invalid time. Please select a time in the future"
                )
        return selected_time

    def clean_vaccine(self):
        child = self.cleaned_data.get("child")
        selected_vaccine = self.cleaned_data.get("vaccine")
        child_age = child.age_in_weeks

        if child_age < selected_vaccine.weeks_minimum_age:
            raise forms.ValidationError("The child is not old enough for this vaccine")
        if child_age > selected_vaccine.weeks_maximum_age:
            raise forms.ValidationError("The child is too old for this vaccine")

        # Check if the parent has already booked an appointment for the selected child
        if child and selected_vaccine:
            existing_appointment = Appointment.objects.filter(
                child=child, vaccine=selected_vaccine
            ).first()

            if existing_appointment:
                raise forms.ValidationError(
                    f"You have already booked a {selected_vaccine.name} appointment for this child."  # noqa: E501
                )
        return selected_vaccine


class RescheduleForm(CustomModelForm):
    class Meta:
        model = Appointment
        fields = ["date", "time"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "time": HourIntervalSelectWidget(attrs={"type": "time"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.time:
            self.initial["time"] = self.instance.time.strftime("%H:%M")

    def clean_date(self):
        selected_date = self.cleaned_data.get("date")
        if selected_date < get_local_now().date():
            raise forms.ValidationError(
                "Invalid date. Please select a date in the future"
            )
        return selected_date

    def clean_time(self):
        selected_time = self.cleaned_data.get("time")
        allowed_times = [interval[0] for interval in HourIntervalSelectWidget.intervals]
        if selected_time.strftime("%H:%M") not in allowed_times:
            raise forms.ValidationError("Please select a valid time.")

        if selected_date := self.cleaned_data.get("date"):
            date_time = combine_date_time(selected_date, selected_time)
            if datetime_less_than_now(date_time):
                raise forms.ValidationError(
                    "Invalid time. Please select a time in the future"
                )
        return selected_time


class CancelForm(CustomModelForm):
    class Meta:
        model = Appointment
        fields = []  # No fields needed for cancelling


class FeedbackForm(CustomModelForm):
    class Meta:
        model = Feedback
        fields = ["title"]
        widgets = {"title": forms.Textarea(attrs={"rows": 5})}
