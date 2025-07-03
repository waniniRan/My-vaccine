from django.db import models, transaction
from Sysadmin.models.HealthFacility import HealthFacility
from Sysadmin.models.FacilityAdmin import FacilityAdmin
from Sysadmin.models.User import User
from django.utils import timezone
from django.core.exceptions import ValidationError

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
 worker_username=models.CharField(max_length=100, unique=True)
 fullname= models.CharField(max_length=200)
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
        db_table = 'Facilityadmin_HealthcareW'
        
 def save(self, *args, **kwargs):
        if not self.pk and not self.worker_id:
            if not self.facility:
                raise ValidationError("Facility must be assigned before saving worker")
                
            with transaction.atomic():
                facility_prefix = self.facility.prefix
                
                # Get next sequential number using select_for_update to prevent race conditions
                facility_locked = HealthFacility.objects.select_for_update().get(pk=self.facility.pk)
                
                # Count all people in this facility
                count = 1  # Facility is 0001
                
                # Count admins
                count += FacilityAdmin.objects.filter(
                    admin_id__startswith=facility_prefix
                ).count()
                
                # Count existing workers (with lock to prevent race conditions)
                count += HealthcareW.objects.select_for_update().filter(
                    worker_id__startswith=facility_prefix
                ).count()
                
                # Get next sequential number
                next_number = count + 1
                self.worker_id = f"{facility_prefix}{str(next_number).zfill(4)}"
                
                # Auto-populate fields
                if not self.worker_username and self.user:
                    self.worker_username = self.user.username
                
        super().save(*args, **kwargs)

 
 def __str__(self):
        return f"{self.fullname} - {self.worker_id} ({self.position})"
     
    
 def activate(self):
        self.status = 'active'
        self.date_left = None
        self.save()
    
 def deactivate(self):
        self.status = 'inactive'
        self.date_left = timezone.now()
        self.save()
