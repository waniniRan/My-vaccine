from django.db import models
from django.utils import timezone
from datetime import date
from Facilityadmin.models import HealthcareW
from django.core.validators import RegexValidator
from Sysadmin.models import Vaccine,User
from HealthcareW.models import Guardian

# This is the child model
# It represents a child in the vaccination system, including personal details and relationships to guardians.
class Child(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    child_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birth_weight = models.DecimalField(max_digits=5, decimal_places=2, help_text="Weight in kg")
    birth_height = models.DecimalField(max_digits=5, decimal_places=2, help_text="Height in cm")
    guardian = models.ForeignKey(Guardian, on_delete=models.CASCADE, related_name='children')
    registered_by = models.ForeignKey('Facilityadmin.HealthcareW', on_delete=models.CASCADE)
    date_registered = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.child_id})"
    
    @property
    def age_in_months(self):
        """Calculate child's age in months"""
        today = date.today()
        months = (today.year - self.date_of_birth.year) * 12 + (today.month - self.date_of_birth.month)
        return months
    
    @property
    def age_in_years(self):
        """Calculate child's age in years"""
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))