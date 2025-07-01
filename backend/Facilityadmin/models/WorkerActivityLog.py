from django.db import models
from Sysadmin.models.FacilityAdmin import FacilityAdmin
from django.utils import timezone
from django.core.exceptions import ValidationError
from Facilityadmin.models.HealthcareW import HealthcareW

# Defining the WorkerActivityLog model
class WorkerActivityLog(models.Model): 
    Action_Choice = [
        ('created', 'Account Created'),
        ('activated', 'Account Activated'),
        ('deactivated', 'Account Deactivated'),
        ('updated', 'Details Updated'),
        ('password_changed', 'Password Changed'),
    ]
    worker = models.ForeignKey(HealthcareW, on_delete=models.CASCADE, related_name='activity_logs' )
    action = models.CharField(max_length=20, choices=Action_Choice)
    performed_by = models.ForeignKey(FacilityAdmin,on_delete=models.SET_NULL,null=True )
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'worker_activity_logs'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.worker.get_full_name()} - {self.action} - {self.timestamp}"
    