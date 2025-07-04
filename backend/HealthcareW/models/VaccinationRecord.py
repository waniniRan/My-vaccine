from django.db import models
#from django.utils import timezone
#from datetime import date
from Facilityadmin.models.HealthcareW import HealthcareW
#from django.core.validators import RegexValidator
from Sysadmin.models.Vaccine import Vaccine
from Sysadmin.models.User import User
from HealthcareW.models.Child import Child

# Describing the VaccinationRecord model
class VaccinationRecord(models.Model):
    
    #Record of vaccines given to children
    recordID= models.CharField(max_length=20, unique=True)
    child_id = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='vaccination_records')
    v_ID = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    administrationDate = models.DateTimeField(auto_now_add=True)  # Use timezone.now for current date and time
    doseNumber= models.IntegerField()
    remarks= models.TextField(blank=True)
    administered_by = models.ForeignKey('Facilityadmin.HealthcareW', on_delete=models.CASCADE)
    side_effects = models.TextField(blank=True)
    

    
    class Meta:
        unique_together = ['child_id', 'v_ID', 'doseNumber']
        ordering =['-administrationDate']
    
    def __str__(self):
        return f"{self.recordID} - {self.child_id.first_name} ({self.v_ID.name} -Dose {self.doseNumber})"
