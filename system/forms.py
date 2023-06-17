from django import forms
from django.contrib.auth.models import User
from .models import Profile
from .models import Child
from .models import Appointment
from .models import  Vaccines
from django.utils import timezone
from django.forms.widgets import DateInput
from datetime import date, time
from django.forms.widgets import CheckboxSelectMultiple
from django.forms.widgets import Select

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password',
                                widget=forms.PasswordInput)
    last_name = forms.CharField(label='Last Name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text=None
    
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name','email']
        
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
             raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
    
    def clean_email(self):
         data = self.cleaned_data['email']
         if User.objects.filter(email=data).exists():
              raise forms.ValidationError('Email already in use.')
         return data

    
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id)\
                            .filter(email=data)
        if qs.exists():
            raise forms.ValidationError('Email already in use')
        return data
    
         
class ProfileEditForm(forms.ModelForm):
        class Meta:
            model = Profile
            fields = ['username', 'date_of_birth', 'phone_number']




class ChildForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ['first_name', 'last_name', 'gender', 'date_of_birth']
        widgets = {
             
             'date_of_birth': DateInput(attrs={'type':'date'})
        }
    
    def clean_date_of_birth(self):
         date_of_birth = self.cleaned_data.get('date_of_birth')

         if date_of_birth > timezone.now().date():
              raise forms.ValidationError("Child's date of birth cannot be in the future")
         
         age_in_months = (timezone.now().date() - date_of_birth).days // 30

         if age_in_months > 18:
              raise forms.ValidationError("Child must be 18 months or below.")
         return date_of_birth
    



#Custom widget to display hour intervals for time field
class HourIntervalSelectWidget(Select):
    def __init__(self, attrs=None, choices=()):
        intervals = [
                    ('08:00', '08:00 AM'),
                    ('09:00', '09:00 AM'),
                    ('10:00', '10:00 AM'),
                    ('11:00', '11:00 AM'),
                    ('12:00', '12:00 PM'),
                    ('13:00', '1:00 PM'),
                    ('14:00', '2:00 PM'),
                    ('15:00', '3:00 PM'),
                    ('16:00', '4:00 PM'),
            # Add more hour intervals as needed
        ]
        super().__init__(attrs, choices=intervals)

#Form for booking appointments
class BookingForm(forms.ModelForm):

    #Field for selecting the child
    child = forms.ModelChoiceField(queryset=Child.objects.none())

    #Field for selecting vaccines
    vaccines = forms.ModelChoiceField(queryset=Vaccines.objects.all(), widget=forms.Select)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['child'].queryset = Child.objects.filter(parent=user)

    #Validate that the selected date is not in the past
    def clean_date(self):
        selected_date = self.cleaned_data['date']
        if selected_date < date.today():
            raise forms.ValidationError("Invalid date. Please select a date in the future")
        return selected_date
    
    #Validate that the selected time is within the allowed range
    # def clean_time(self):
    #     selected_time = self.cleaned_data['time']
    #     if not (time(7, 0) <= selected_time <= time(16, 0)):
    #         raise forms.ValidationError("Invalid time. Booking times are available between 7am and 4pm")
    #     return selected_time
    
    #Validate the overall form data
    def clean(self):
        cleaned_data = super().clean()
        selected_date = cleaned_data.get('date')
        selected_time = cleaned_data.get('time')

        if selected_date:
            #Check if the selected date is fully booked
            appointment_count = Appointment.objects.filter(date=selected_date).count()
            if appointment_count >= 50:
                raise forms.ValidationError("This date is fully booked. Please select another date.")
            
            #Check if the selected time is already booked
            # existing_appointment = Appointment.objects.filter(date=selected_date, time=selected_time).first()
            # if existing_appointment:
            #     raise forms.ValidationError("This time slot is already booked. Please select another time")

        return cleaned_data

    class Meta:
        model = Appointment
        fields = ['child', 'date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': HourIntervalSelectWidget(attrs={'type': 'time'}),
        }

    

class RescheduleForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': HourIntervalSelectWidget(attrs={'type': 'time'}),
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