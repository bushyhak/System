from django import forms
from django.contrib.auth.models import User
from .models import Profile
from .models import Child
from django.utils import timezone
from django.forms.widgets import DateInput

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
            fields = ['username', 'date_of_birth', 'phone_number', 'photo']


class ChildForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ['first_name', 'last_name', 'gender', 'date_of_birth']
        widgets = {
             
             'date_of_birth': DateInput(attrs={'type':'date'})
        }
    
    def clean_date_of_birth(self):
         date_of_birth = self.cleaned_data.get('date_of_birth')
         age_in_months = (timezone.now().date() - date_of_birth).days // 30

         if age_in_months > 18:
              raise forms.ValidationError("Child must be 18 months or below.")
         return date_of_birth