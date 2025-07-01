from django.db import models
from django.utils import timezone
from datetime import date
from django.core.validators import RegexValidator
from HealthcareW.models.Child import Child 

# Defining the GrowthCurve model
class GrowthCurve(models.Model):
    
   # Growth curve data for tracking child development

    CURVE_TYPE_CHOICES = [
        ('WEIGHT_AGE', 'Weight for Age'),
        ('HEIGHT_AGE', 'Height for Age'),
        ('WEIGHT_HEIGHT', 'Weight for Height'),
    ]
    
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='growth_curves')
    curve_type = models.CharField(max_length=20, choices=CURVE_TYPE_CHOICES)
    percentile = models.DecimalField(max_digits=5, decimal_places=2, help_text="Child's percentile (0-100)")
    z_score = models.DecimalField(max_digits=5, decimal_places=2, help_text="Standard deviation from mean")
    date_calculated = models.DateField()
    is_normal_range = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['child', 'curve_type', 'date_calculated']
    
    def __str__(self):
        return f"{self.child.first_name} - {self.get_curve_type_display()} ({self.percentile}th percentile)"
#END 