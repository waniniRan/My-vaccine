from django.db import models
from django.utils import timezone
from datetime import date
from Facilityadmin.models import HealthcareW
from django.core.validators import RegexValidator
from Sysadmin.models import Vaccine,User

# This is the main model, it contains the healthcare worker's interface to register the guardian and their child
#It contains the appointments, the notifications, the growth curve and all the information about vaccines
# they will also have two interfaces: A web interface and an app interface

class Guardian(models.Model): 
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name= 'Guardian'
        )
    national_id = models.CharField( 
        max_length=20, 
        unique=True, 
        validators=[RegexValidator(r'^\d+$', 'National ID must contain only numbers')] )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=128)  # Will be hashed
    date_registered = models.DateTimeField(auto_now_add=True)
    registered_by = models.ForeignKey(HealthcareW, on_delete=models.CASCADE) #Facilityadmin.HealthcareW
    is_active = models.BooleanField(default=True)
    
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} (ID: {self.national_id})"

class Child(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    child_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birth_weight = models.DecimalField(max_digits=5, decimal_places=2, help_text="Weight in kg")
    birth_height = models.DecimalField(max_digits=5, decimal_places=2, help_text="Height in cm")
    guardian = models.ForeignKey(Guardian, on_delete=models.CASCADE, related_name='children')
    registered_by = models.ForeignKey('Facilityadmin.HealthcareW', on_delete=models.CASCADE)
    date_registered = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.child_id})"
    
    @property
    def age_in_months(self):
        """Calculate child's age in months"""
        today = date.today()
        months = (today.year - self.date_of_birth.year) * 12 + (today.month - self.date_of_birth.month)
        return months
    
    @property
    def age_in_years(self):
        """Calculate child's age in years"""
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

class VaccinationRecord(models.Model):
    
    #Record of vaccines given to children
    Vaccination_record_ID= models.CharField(max_length=20, unique=True)
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='vaccination_records')
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    date_administered = models.DateField()
    administered_by = models.ForeignKey('Facilityadmin.HealthcareW', on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    side_effects = models.TextField(blank=True)
    date_recorded = models.DateTimeField(auto_now_add=True)
    remarks= models.TextField(blank=True)
    dose_number= models.IntegerField()

    
    class Meta:
        unique_together = ['child', 'vaccine', 'dose_number']
        ordering =['-date_administered']
    
    def __str__(self):
        return f"{self.Vaccination_record_ID} - {self.child.first_name} ({self.vaccine.name} -Dose {self.dose_number})"

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

class Appointment(models.Model):
    #Vaccination appointments   
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='appointments')
    scheduled_date = models.DateTimeField()
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    healthcare_worker = models.ForeignKey('Facilityadmin.HealthcareW', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey('Facilityadmin.HealthcareW', on_delete=models.CASCADE, related_name='created_appointments')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['scheduled_date']
    
    def __str__(self):
        return f"{self.child.first_name} - {self.vaccine_type.name} ({self.scheduled_date.date()})"

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

class HealthcareWorkerSession(models.Model):
    
  #  Track healthcare worker login sessions
    
    healthcare_worker = models.ForeignKey('Facilityadmin.HealthcareW', on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.healthcare_worker.first_name} - {self.login_time}"


