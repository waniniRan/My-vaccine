from django import forms
from django.contrib.auth.models import User
from .models import HealthFacility,Vaccine
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import HealthFacility


class healthfacilityform(forms.ModelForm):
    class Meta:
        model = HealthFacility
        fields = ['name', 'location', 'phone', 'email']


class Vaccinationform(forms.ModelForm):
    class Meta:
        model = Vaccine
        fields = ['name',  'diseasePrevented', 'dose', 'description', 'recommended age']

#FACILITY ADMIN
User = get_user_model()

class FacilityAdminCreationForm(forms.Form):
    # Facility Information
    facility_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    facility_type = forms.ChoiceField(
        choices=HealthFacility.FACILITY_TYPES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # Admin Account Details
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8,
        help_text="Minimum 8 characters"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords don't match")
        
        return cleaned_data
    