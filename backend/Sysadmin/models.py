from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import transaction
from django.core.exceptions import ValidationError

#DEFINE THE ALL USERS 
class User(AbstractUser):
    class Role(models.TextChoices):
        SYSTEM_ADMIN = 'SYSTEM_ADMIN', 'System Administrator'
        FACILITY_ADMIN = 'FACILITY_ADMIN', 'Facility Administrator'
        WORKER = 'HEALTHCARE WORKER', 'Worker'
        USER = 'GUARDIAN', 'Guardian'
    
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER
    )
    must_change_password = models.BooleanField(default=True)
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='sysadmin_user_set',  # Add this
        related_query_name='sysadmin_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='sysadmin_user_set',  # Add this
        related_query_name='sysadmin_user',
    )
    def clean(self):
        """Ensure system admins have is_staff and is_superuser set correctly"""
        if self.role == self.Role.SYSTEM_ADMIN:
            self.is_staff = True
            self.is_superuser = True
        super().clean()
    
    def save(self, *args, **kwargs):
        self.full_clean()  # Runs clean() method before saving
        super().save(*args, **kwargs)
#END

# REPORTS OF THE SYSTEM
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

#Add HEALTHFACILITY AND VACCINE
#HEALTHFACILITY
class HealthFacility(models.Model):
    FACILITY_TYPES = (
        ('HOSPITAL', 'Hospital'),
        ('CLINIC', 'Clinic'),
        ('HEALTH_CENTER', 'Health Center'),
    )
    prefix=models.CharField(max_length=1, unique=True, editable=False) #eg., K , M
    ID = models.CharField(max_length=15, unique=True, editable=False)
    name = models.CharField(max_length=200)
    facility_type = models.CharField(max_length=50, choices=FACILITY_TYPES)
    location = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    admin = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        related_name='managed_facility',
        limit_choices_to={'role': User.Role.FACILITY_ADMIN}
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='created_facilities'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.pk: #new instances   
         with transaction.atomic():
           self.prefix = self._generate_next_prefix()
           self.ID = f"{self.prefix}0001" #facility gets 0001
        super().save(*args, **kwargs)

    def _generate_next_prefix(self): #prefix A,B,C .......
        last_facility = HealthFacility.objects.select_for_update().order_by('prefix').last()
        if not last_facility:
          return 'A'
        last_prefix = last_facility.prefix
        if last_prefix == 'Z':
          raise ValueError("All prefixes A-Z are used. Please expand logic.")
        return chr(ord(last_prefix) + 1)
    @property
    def facility_prefix(self):
        return self.prefix

    def __str__(self):
        return f"{self.name} {self.ID}"
#END

#VACCINE
class Vaccine(models.Model):
    name = models.CharField(max_length=100)
    v_ID = models.CharField(max_length=10)
    description = models.TextField(blank=True)
    dosage = models.CharField(max_length=50)  # "2 doses", "Single dose", etc.
    diseasePrevented = models.CharField(max_length=100)
    recommended_age= models.CharField(max_length=20)
    facility = models.ManyToManyField( HealthFacility,related_name='vaccines')
    created_by = models.ForeignKey(User, on_delete=models.PROTECT,related_name='created_vaccines')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
         facilities = ", ".join([f.name for f in self.facility.all()[:3]])  # Show first 3 facilities
         if self.facility.count() > 3:
          facilities += f" and {self.facility.count() - 3} more"
         return f"{self.name} - Available at: {facilities}" if facilities else f"{self.name} - No facilities assigned"    
    def __str__ (self):
        return f"{self.name} ({self.v_ID}) - {self.recommended_age} months"
#END     

#FACILITY ADMIN
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
    
    