from django.db import models
from django.contrib.auth.models import AbstractUser
#from django.db import transaction
#from django.core.exceptions import ValidationError


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
    class Meta:
        db_table= 'auth_user'
        
    def clean(self):
        """Ensure system admins have is_staff and is_superuser set correctly"""
        if self.role == self.Role.SYSTEM_ADMIN:
            self.is_staff = True
            self.is_superuser = True
        elif self.role == self.Role.FACILITY_ADMIN:
            self.is_staff = True
            self.is_superuser = False
        else:
            self.is_staff = False
            self.is_superuser = False
        super().clean()
    
    def save(self, *args, **kwargs):
        self.full_clean()  # Runs clean() method before saving
        super().save(*args, **kwargs)

    
    @property
    def is_system_admin(self):
        return self.role == self.Role.SYSTEM_ADMIN
    
    @property
    def is_facility_admin(self):
        return self.role == self.Role.FACILITY_ADMIN
    
    @property
    def is_healthcare_worker(self):
        return self.role == self.Role.WORKER
    
    @property
    def is_user(self):
        return self.role == self.Role.USER
    
#SYSTEM ADMINISTRATION PERMISSIONS
    def can_create_facility_admin(self):
        """Check if user can create facility admins"""
        return self.is_system_admin
    def can_create_health_facility(self):
        """Check if user can create health facilities"""
        return self.is_system_admin
    def can_create_vaccine(self):
        """Check if user can create vaccines"""
        return self.is_system_admin
    def can_view_facility_admins(self):
        """Check if user can view facility admins"""
        return self.is_system_admin 
    def can_view_system_reports(self):
        """Check if user can view system reports"""
        return self.is_system_admin 
    
#FACILITY ADMINISTRATION PERMISSIONS
    def can_create_healthcare_worker(self):
        """Check if user can create healthcare workers"""
        return self.is_facility_admin
    def can_view_system_reports(self):
        """Check if user can view system reports"""
        return self.is_facility_admin
    
    

#HEALTHCAREW PERMISSIONS
    def can_create_guardian(self):
        """Check if user can create guardians"""
        return self.is_healthcare_worker
    def can_create_child(self):
        """Check if user can create child"""
        return self.is_healthcare_worker
    
#Guardian PERMISSIONS
    def can_view_child_vaccination(self):
        """Check if user can view child's vaccination records"""
        return  self.is_user
    def can_view_child_vaccination_history(self):
        """Check if user can view child's vaccination history"""
        return self.is_user
    def can_view_child_vaccination_schedule(self):
        """Check if user can view child's vaccination schedule"""
        return  self.is_user
    def can_view_child_growth_records(self):
        """Check if user can view child's growth records"""
        return self.is_user
    def can_view_child_growth_curve(self):
        """Check if user can view child's growth curve"""
        return  self.is_user  
    def can_view_notifications(self):
        """Check if user can view notifications"""
        return self.is_user
    def can_view_guardian_profile(self):
        """Check if user can view guardian profile"""
        return self.is_user
    
#END