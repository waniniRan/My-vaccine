from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import transaction
from django.core.exceptions import ValidationError
from Sysadmin.models import User

#Defining the SystemActivityLog model 
class SystemActivityLog(models.Model):

    """
    Log model to track system administrator activities
    """
    ACTION_CHOICES = [
        ('facility_created', 'Facility Created'),
        ('facility_updated', 'Facility Updated'),
        ('facility_deactivated', 'Facility Deactivated'),
        ('admin_created', 'Facility Admin Created'),
        ('admin_updated', 'Facility Admin Updated'),
        ('vaccine_created', 'Vaccine Created'),
        ('vaccine_updated', 'Vaccine Updated'),
        ('report_generated', 'Report Generated'),
    ]
    admin = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='activity_logs'
    )
    action = models.CharField(max_length=30, choices=ACTION_CHOICES)
    target_type = models.CharField(max_length=50)  # 'facility', 'vaccine', 'admin'
    target_id = models.CharField(max_length=50)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        db_table = 'system_activity_logs'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.admin.username} - {self.action} - {self.timestamp}"
    
    