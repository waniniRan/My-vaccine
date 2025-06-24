from django.db import models
from Sysadmin.models import HealthFacility,FacilityAdmin,User
from django.utils import timezone


#In the facility admin app we will set up the information for our healthcare worker
#Facility admin has been registered by the system admin and here they are supposed to add this worker and monitor them

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

class HealthcareW(models.Model):   
 user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name= 'Worker'
        )    
 Position_Choice= [
        ('doctor', 'Doctor'),
        ('nurse', 'Nurse'),
        ]
 Status_Choice= [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    ]   
 worker_id= models.CharField(max_length=15, unique=True, primary_key=True)
 username=models.CharField(max_length=100, unique=True)
 first_name= models.CharField(max_length=30)
 last_name=models.CharField(max_length=30)
 email=models.EmailField(blank=True)
 phone_number= models.CharField(max_length=15, blank=True)
 position= models.CharField(max_length=15, choices=Position_Choice)
 facility= models.ForeignKey(HealthFacility, on_delete=models.CASCADE, related_name='workers')
 Facility_admin= models.ForeignKey(FacilityAdmin, on_delete=models.CASCADE, related_name='managed_workers')
 temporary_password= models.CharField(max_length=120)
 password_changed= models.BooleanField(default=False)
 status= models.CharField(max_length=10, choices= Status_Choice)
 date_joined = models.DateTimeField(default=timezone.now)
 date_left = models.DateTimeField(null=True, blank=True)
 created_at = models.DateTimeField(auto_now_add=True)
 updated_at = models.DateTimeField(auto_now=True)
 


 class Meta:
        db_table = 'healthcare_workers'
        ordering = ['last_name', 'first_name']
    
 def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.position}"
     
 def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
 def activate(self):
        self.status = 'active'
        self.date_left = None
        self.save()
    
 def deactivate(self):
        self.status = 'inactive'
        self.date_left = timezone.now()
        self.save()

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