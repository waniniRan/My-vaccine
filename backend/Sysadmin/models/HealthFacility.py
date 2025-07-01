from django.db import models
#from django.contrib.auth.models import AbstractUser
from django.db import transaction
#from django.core.exceptions import ValidationError
from Sysadmin.models import User
from Sysadmin.models import HealthFacility

# Defining the HealthFacility model
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