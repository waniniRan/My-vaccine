from django.db import models
from django.utils import timezone
from datetime import date
from Facilityadmin.models.HealthcareW import HealthcareW
from django.core.validators import RegexValidator
from Sysadmin.models.User import User

#Description of the Guardian model:
# The Guardian model represents a guardian of a child in the system.
class Guardian(models.Model): 
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name= 'Guardian'
        )
    national_id = models.CharField( 
        max_length=20, 
        unique=True, 
        validators=[RegexValidator(r'^\d+$', 'National ID must contain only numbers')] )
    fullname = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    temporary_password = models.CharField(max_length=128)  # Will be hashed
    password_changed = models.BooleanField(default=True)
    date_registered = models.DateTimeField(auto_now_add=True)
    registered_by = models.ForeignKey(HealthcareW, on_delete=models.CASCADE) #Facilityadmin.HealthcareW
    is_active = models.BooleanField(default=True)
    
    
    def __str__(self):
        return f"{self.fullname} (ID: {self.national_id})"