from django.db import models
from Sysadmin.models import User
#from django.contrib.auth.models import AbstractUser
#from django.db import transaction
#from django.core.exceptions import ValidationError

class SystemReport(models.Model):
    REPORT_TYPES = (
        ('USER_ACTIVITY', 'User Activity Log'),
        ('LOGIN_HISTORY', 'Login History'),
        ('PASSWORD_CHANGES', 'Password Changes'),
        ('ADMIN_ACTIONS', 'Admin Actions'),
        ('FACILITY_SUMMARY', 'Facility Summary'),
    )
    report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
    generated_by = models.ForeignKey(User, on_delete=models.PROTECT)
    generated_at = models.DateTimeField(auto_now_add=True)
    report_file = models.FileField(upload_to='system_reports/')
    parameters = models.JSONField(default=dict)  # Stores report filters/options
    is_downloaded = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-generated_at']
#END