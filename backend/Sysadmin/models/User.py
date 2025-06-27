from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import transaction
from django.core.exceptions import ValidationError


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