from Sysadmin.models import HealthFacility,FacilityAdmin,User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import models, transaction

# Defining the FacilityReport model
class FacilityReport(models.Model):
    REPORT_TYPES = [
        ('vaccination_coverage', 'Vaccination Coverage'),
        ('child_registration', 'Child Registration'),
        ('growth_monitoring', 'Growth Monitoring'),
        ('overdue_vaccinations', 'Overdue Vaccinations'),
    ]
    facility=models.ForeignKey(HealthFacility,on_delete=models.CASCADE)
    report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
    generated_by = models.ForeignKey(User, on_delete=models.PROTECT)
    generated_at = models.DateTimeField(auto_now_add=True)
    report_file = models.FileField(upload_to='facility_reports/')
    parameters = models.JSONField(default=dict)  # Stores report filters/options
    is_downloaded = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-generated_at']
