from django.db import models
from django.utils import timezone
from datetime import date
from Facilityadmin.models import HealthcareW
from django.core.validators import RegexValidator
from Sysadmin.models import Vaccine,User
from HealthcareW.models import Child

# Describing the VaccinationRecord model
class VaccinationRecord(models.Model):
    
    #Record of vaccines given to children
    Vaccination_record_ID= models.CharField(max_length=20, unique=True)
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='vaccination_records')
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    date_administered = models.DateField()
    administered_by = models.ForeignKey('Facilityadmin.HealthcareW', on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    side_effects = models.TextField(blank=True)
    date_recorded = models.DateTimeField(auto_now_add=True)
    remarks= models.TextField(blank=True)
    dose_number= models.IntegerField()

    
    class Meta:
        unique_together = ['child', 'vaccine', 'dose_number']
        ordering =['-date_administered']
    
    def __str__(self):
        return f"{self.Vaccination_record_ID} - {self.child.first_name} ({self.vaccine.name} -Dose {self.dose_number})"
