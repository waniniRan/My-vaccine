from django.db import models
from django.utils import timezone
from datetime import date
from Facilityadmin.models import HealthcareW
from django.core.validators import RegexValidator
from Sysadmin.models import Vaccine,User
from HealthcareW.models import Child, Appointment, Guardian

# Notification model
class Notification(models.Model):
    
    #Notifications for appointments
    
    NOTIFICATION_TYPE_CHOICES = [
        ('WEEK_BEFORE', 'One Week Before'),
        ('TWO_DAYS_BEFORE', 'Two Days Before'),
        ('MISSED_APPOINTMENT', 'Missed Appointment'),
    ]
    
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='notifications')
    guardian = models.ForeignKey(Guardian, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    message = models.TextField()
    is_sent = models.BooleanField(default=False)
    date_sent = models.DateTimeField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.guardian.first_name} - {self.get_notification_type_display()} ({self.appointment.scheduled_date.date()})"