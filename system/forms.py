from django import forms
from django.contrib.auth.models import User
from .models import Profile, Child, Appointment
from django.utils import timezone
from datetime import date
from django.forms.widgets import Select, DateInput
from django.contrib.auth.forms import UserCreationForm


class CustomModelForm(forms.ModelForm):
    """Extend the django ModelForm, adding "form-control" css class and a placeholder"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name.lower().find("date") >= 0:
                field.widget.input_type = "date"
            if field_name.lower().find("phone") >= 0:
                field.widget.input_type = "tel"

            self.add_class(field, "form-control")

            if not field.widget.attrs.get("placeholder"):
                field.widget.attrs["placeholder"] = "Enter %s..." % field.label.lower()

            if self.has_error(field_name):
                self.add_class(field, "is-invalid")

    def add_class(self, field, css_class):
        if field.widget.attrs.get("class"):
            field.widget.attrs["class"] += f" {css_class}"
        else:
            field.widget.attrs["class"] = css_class


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
            if date_of_birth > timezone.now().date():
                raise forms.ValidationError("Date of birth cannot be in the future")

        return date_of_birth


class ChildForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ["first_name", "last_name", "gender", "date_of_birth"]
        widgets = {"date_of_birth": DateInput(attrs={"type": "date"})}

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get("date_of_birth")
        if not date_of_birth:  # prevents errors below if date_of_birth is None
            return date_of_birth

        if date_of_birth > timezone.now().date():
            raise forms.ValidationError("Child's date of birth cannot be in the future")

        age_in_months = (timezone.now().date() - date_of_birth).days // 30

        if age_in_months > 18:
            raise forms.ValidationError("Child must be 18 months or below.")

        return date_of_birth


# Custom widget to display hour intervals for time field
class HourIntervalSelectWidget(Select):
    def __init__(self, attrs=None, choices=()):
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
        super().__init__(attrs, choices=intervals)


# Form for booking appointments
class BookingForm(forms.ModelForm):
    child = forms.ModelChoiceField(queryset=Child.objects.none())

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        self.request = kwargs.pop("request")
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields["child"].queryset = Child.objects.filter(parent=user)

    # Validate that the selected date is not in the past
    def clean_date(self):
        selected_date = self.cleaned_data["date"]
        if selected_date < date.today():
            raise forms.ValidationError(
                "Invalid date. Please select a date in the future"
            )
        return selected_date

    def clean(self):
        cleaned_data = super().clean()
        selected_date = cleaned_data.get("date")
        selected_time = cleaned_data.get("time")
        child = cleaned_data.get("child")
        parent = self.request.user
        selected_vaccine = cleaned_data.get("vaccines")  # noqa: F841

        # Check if the parent has already booked an appointment for the selected child
        if selected_date and selected_time and child:
            existing_appointment = Appointment.objects.filter(
                child=child, parent=parent
            ).first()

            if existing_appointment:
                raise forms.ValidationError(
                    "You have already booked an appointment for this child."
                )

        # Check if the selected date is fully booked
        if selected_date:
            appointment_count = Appointment.objects.filter(date=selected_date).count()
            if appointment_count >= 50:
                raise forms.ValidationError(
                    "This date is fully booked. Please select another date."
                )

        return cleaned_data

    class Meta:
        model = Appointment
        fields = ["child", "date", "time"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "time": HourIntervalSelectWidget(attrs={"type": "time"}),
        }


class RescheduleForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["date", "time"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "time": HourIntervalSelectWidget(attrs={"type": "time"}),
        }


class CancelForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = []  # No fields needed for canceling

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.error_css_class = 'error'

    # def is_error(self, field_name):
    #     return bool(self.errors.get(field_name, False))
