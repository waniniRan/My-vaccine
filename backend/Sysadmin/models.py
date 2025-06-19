from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


#DEFINE THE ALL USERS 
class User(AbstractUser):
    class Role(models.TextChoices):
        SYSTEM_ADMIN = 'SYSTEM_ADMIN', 'System Administrator'
        FACILITY_ADMIN = 'FACILITY_ADMIN', 'Facility Administrator'
        WORKER = 'HEALTHCARE WORKER', 'Worker'
        USER = 'GUARDIAN', 'User'
    
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
    ID = models.CharField(max_length=10, unique=True, editable=False)
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
         self.prefix = self._generate_next_prefix()
         self.ID = f"{self.prefix}0000"
        super().save(*args, **kwargs)   
    def _generate_next_prefix(self):
        existing_prefixes = HealthFacility.objects.values_list('prefix', flat=True)
        for ascii_code in range(ord('A'), ord('Z') + 1):
            candidate = chr(ascii_code)
            if candidate not in existing_prefixes:
                return candidate
        raise ValueError("All prefixes A-Z are used. Please expand logic.")
    def __str__(self):
        return f"{self.name} {self.ID} ({self.get_facility_type_display()})"
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
        return f"{self.name} at {self.facility.name}"
#END
