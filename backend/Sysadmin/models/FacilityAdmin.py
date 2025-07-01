from django.db import models
#from django.contrib.auth.models import AbstractUser
from django.db import transaction
from django.core.exceptions import ValidationError
from Sysadmin.models import User
from Sysadmin.models import HealthFacility

#Defining the FacilityAdmin model
class FacilityAdmin(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name= 'facility_admin'
        )
    facility = models.OneToOneField(HealthFacility, on_delete=models.CASCADE)
    admin_id = models.CharField(max_length=15, unique=True, editable=False)
    admin_username=models.CharField(max_length=150, unique=True)
    phone= models.CharField(max_length=20, blank=True)
    fullname= models.CharField(max_length=120)
    is_active=models.BooleanField(default=True)
    temporary_password = models.CharField(max_length=128)
    password_changed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
  
    def save(self, *args, **kwargs):
        if not self.pk:  # New instance
            if not self.facility:
                raise ValidationError("Facility must be assigned before saving admin")
            
            with transaction.atomic():
                # Admin always gets the facility prefix + 0002
                self.admin_id = f"{self.facility.prefix}0002"

                if FacilityAdmin.objects.filter(admin_id=self.admin_id).exists():
                    raise ValidationError(f"Admin already exists for facility {self.facility.prefix}")
                
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.username} - {self.admin_id} (Facility Admin)"
#END