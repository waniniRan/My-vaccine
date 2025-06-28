from django.db import models
from django.utils import timezone
from datetime import date
from Facilityadmin.models import HealthcareW
from django.core.validators import RegexValidator
from Sysadmin.models import Vaccine,User
from HealthcareW.models import Child

# This is the appointment model
class Appointment(models.Model):
    #Vaccination appointments   
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='appointments')
    scheduled_date = models.DateTimeField()
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    healthcare_worker = models.ForeignKey('Facilityadmin.HealthcareW', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey('Facilityadmin.HealthcareW', on_delete=models.CASCADE, related_name='created_appointments')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['scheduled_date']
    
    def __str__(self):
        return f"{self.child.first_name} - {self.vaccine_type.name} ({self.scheduled_date.date()})"