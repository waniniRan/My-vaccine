from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import transaction
from django.core.exceptions import ValidationError
from Sysadmin.models import User
from Sysadmin.models import HealthFacility

#Defining the Vaccine model
class Vaccine(models.Model):
    name = models.CharField(max_length=100)
    v_ID = models.CharField(max_length=10)
    description = models.TextField(blank=True)
    dosage = models.CharField(max_length=50)  # "2 doses", "Single dose", etc.
    diseasePrevented = models.CharField(max_length=100)
    recommended_age= models.CharField(max_length=20)
    facility = models.ManyToManyField( HealthFacility,related_name='vaccines')
    created_by = models.ForeignKey(User, on_delete=models.PROTECT,related_name='created_vaccines')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
         facilities = ", ".join([f.name for f in self.facility.all()[:3]])  # Show first 3 facilities
         if self.facility.count() > 3:
          facilities += f" and {self.facility.count() - 3} more"
         return f"{self.name} - Available at: {facilities}" if facilities else f"{self.name} - No facilities assigned"    
    def __str__ (self):
        return f"{self.name} ({self.v_ID}) - {self.recommended_age} months"
#END     