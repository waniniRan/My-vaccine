from django.db import models
from django.utils import timezone
from datetime import date
from Facilityadmin.models.HealthcareW import HealthcareW
from django.core.validators import RegexValidator
from HealthcareW.models.Child import Child

# Description of growth record model
class GrowthRecord(models.Model):
    #Growth tracking for children
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='growth_records')
    date_recorded = models.DateField()
    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text="Weight in kg")
    height = models.DecimalField(max_digits=5, decimal_places=2, help_text="Height in cm")
    recorded_by = models.ForeignKey('Facilityadmin.HealthcareW', on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['child', 'date_recorded']
        ordering = ['-date_recorded']
    
    def __str__(self):
        return f"{self.child.first_name} - {self.date_recorded} (W: {self.weight}kg, H: {self.height}cm)"
