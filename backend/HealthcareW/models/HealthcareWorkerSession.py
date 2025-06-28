from django.db import models
from django.utils import timezone
from datetime import date
from Facilityadmin.models import HealthcareW
from django.core.validators import RegexValidator
from Sysadmin.models import Vaccine,User

# Desciption of HealthcareWorkerSession model
class HealthcareWorkerSession(models.Model):
    
  #  Track healthcare worker login sessions
    
    healthcare_worker = models.ForeignKey('Facilityadmin.HealthcareW', on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.healthcare_worker.first_name} - {self.login_time}"
