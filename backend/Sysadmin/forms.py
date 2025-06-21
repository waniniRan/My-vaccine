from django import forms
from django.contrib.auth.models import User
from .models import HealthFacility,Vaccine
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import HealthFacility, Vaccine
import re


class healthfacilityform(forms.ModelForm):
    class Meta:
        model = HealthFacility
        fields = ['name','facility_type', 'location', 'phone', 'email']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter facility name'
            }),
            'facility_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter facility location'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+254 XXX XXX XXX'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'facility@example.com'
            })
        }
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # Remove spaces and special characters for validation
            clean_phone = re.sub(r'[\s\-\(\)]', '', phone)
            
            # Check for Kenyan phone number format
            if not re.match(r'^(\+254|0)[17]\d{8}$', clean_phone):
                raise ValidationError(
                    "Please enter a valid Kenyan phone number (e.g., +254 XXX XXX XXX or 0XXX XXX XXX)"
                )
        return phone
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Check if email is already used by another facility
            if self.instance.pk:
                # Editing existing facility
                if HealthFacility.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                    raise ValidationError("This email is already used by another facility")
            else:
                # Creating new facility
                if HealthFacility.objects.filter(email=email).exists():
                    raise ValidationError("This email is already used by another facility")
        return email



class Vaccinationform(forms.ModelForm):
    class Meta:
        model = Vaccine
        fields = ['name',  'diseasePrevented', 'dosage', 'description', 'recommended_age']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter vaccine name'
            }),
            'diseasePrevented': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Disease prevented by this vaccine'
            }),
            'dosage': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Single dose, 2 doses, etc.'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter vaccine description...'
            }),
            'recommended_age': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 6-12 months, Adults, etc.'
            })
        }
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show active facilities
        self.fields['facility'].queryset = HealthFacility.objects.filter(is_active=True)
        
        # Make facility field required
        self.fields['facility'].required = True
        self.fields['facility']= kwargs.get('facility', None)
        self.fields['facility'].help_text = "Select at least one facility where this vaccine is available"
     '''
    def clean_facility(self):
        facilities = self.cleaned_data.get('facility')
        if not facilities:
            raise ValidationError("Please select at least one facility")
        return facilities


#FACILITY ADMIN
User = get_user_model()

class FacilityAdminCreationForm(forms.Form):
    # Facility Information
    facility_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter facility name'
            }),
        help_text = "Enter the name of the Health facility"
    )

    facility_type = forms.ChoiceField(
        choices=HealthFacility.FACILITY_TYPES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text= "Select the type of health facility"
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

