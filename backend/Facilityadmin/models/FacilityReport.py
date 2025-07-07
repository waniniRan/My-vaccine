from Sysadmin.models.HealthFacility import HealthFacility
from Sysadmin.models.User import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import models

# Defining the FacilityReport model
class FacilityReport(models.Model):
    REPORT_TYPES = [
        ('vaccination_coverage', 'Vaccination Coverage'),
        ('child_registration', 'Child Registration'),
        ('growth_monitoring', 'Growth Monitoring'),
        ('overdue_vaccinations', 'Overdue Vaccinations'),
    ]
    facility=models.ForeignKey(HealthFacility,on_delete=models.CASCADE, to_field='ID', db_column='facility_id')
    report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
    generated_by = models.ForeignKey(User, on_delete=models.PROTECT)
    generated_at = models.DateTimeField(auto_now_add=True)
    report_file = models.FileField(upload_to='facility_reports/')
    parameters = models.JSONField(default=dict)  # Stores report filters/options
    is_downloaded = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-generated_at']
