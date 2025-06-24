#This is where all the serialisers of the project are stored
from rest_framework import serializers
from Sysadmin.models import HealthFacility, Vaccine ,User
from Facilityadmin.models import HealthcareW,FacilityReport,HealthFacility,FacilityAdmin
from HealthcareW.models import Guardian,Child,VaccinationRecord,GrowthRecord,Notification
from django.contrib.auth import get_user_model
from django.db import IntegrityError # Useful for catching unique constraint errors
import re # For phone number validation

# Get the custom user model (defined by AUTH_USER_MODEL in settings.py)
User = get_user_model()



#These serializers are for the System admin, it containes everything the manage
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    managed_facility_name = serializers.CharField(source =' managed_facility.name', read_only= True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'managed_facility_name', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', User.Role.USER)
        )
        return user

class HealthFacilitySerializer(serializers.ModelSerializer):
#Serializer for the HealthFacility model. Handles validation andserialization/deserialization of HealthFacility instances.
    
    class Meta:
        model = HealthFacility
        fields = ['id', 'name', 'facility_type', 'location', 'phone', 'email']
        # 'id' is typically included in API responses for unique identification.

    def validate_phone(self, value):
        
# Validates the provided phone number to ensure it adheres to Kenyan phone number formats. Removes spaces and special characters before validation.
        if value:
         clean_phone = re.sub(r'[\s\-\(\)]', '', value)

            # Check for common Kenyan phone number patterns:
        if not re.match(r'^(?:(?:\+254|0)[17]\d{8}|[17]\d{8})$', clean_phone):
                raise serializers.ValidationError(
                    "Please enter a valid Kenyan phone number (e.g., +254 XXX XXX XXX, 0XXX XXX XXX, or 7XXX XXX XXX)." )
        return value

    def validate_email(self, value):
#Validates the email address to ensure it is unique across all health facilities,excluding the current instance if it's an update operation.
        if value:
            # Query for existing facilities with the given email
            query = HealthFacility.objects.filter(email=value)

            # If an instance is being updated, exclude that instance from the check
            if self.instance: # self.instance holds the object being updated (if any)
                query = query.exclude(pk=self.instance.pk)
            # If any other facility already uses this email, raise a validation error
            if query.exists():
                raise serializers.ValidationError("This email is already used by another facility.")
        return value

class VaccineSerializer(serializers.ModelSerializer):
#Serializer for the Vaccine model. Handles validation and serialization/deserialization of Vaccine instances.  
    facilities = serializers.PrimaryKeyRelatedField(
        queryset=HealthFacility.objects.all(),
        many=True,  # Set to True for ManyToMany relationships
        required=False, # Set to True if a vaccine must be linked to at least one facility
        help_text="IDs of the health facilities where this vaccine is available."
    )

    class Meta:
        model = Vaccine
        fields = ['id', 'name', 'diseasePrevented', 'dosage', 'description', 'recommended_age', 'facilities']
       
    def validate_facilities(self, value):
        #Ensures that if the 'facilities' field is provided, it's not empty.
        #This validation only applies if `required=False` for the field above,
        #but you want to enforce a minimum of one if the field is present.
        #If `required=True`, DRF's default validation handles empty lists.
        # If the facilities field is required in your model/serializer
        # and it's an empty list, this will catch it.
        if not value:
            raise serializers.ValidationError("Please select at least one facility for the vaccine.")
        return value

class FacilityAdminCreationSerializer(serializers.Serializer):
    """
    Serializer for creating a new HealthFacility and a corresponding
    Facility Admin User account simultaneously, reusing HealthFacilitySerializer.
    """
    
    facility_details = HealthFacilitySerializer(
        write_only=True, # Important: This data is only for input, not returned on output.
                         # If you want to return the created facility, you'd handle it in create().
        help_text="Details for the new health facility (name, type, location, phone, email)."
    )

    # Admin User Account Details
    username = serializers.CharField(
        max_length=150,
        help_text="Desired username for the facility admin account."
    )
    email_admin = serializers.EmailField(
        help_text="Email address for the facility admin account."
    )
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        help_text="Minimum 8 characters for the admin password."
    )
    confirm_password = serializers.CharField(
        write_only=True,
        help_text="Confirm the admin password."
    )

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def validate_email_admin(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered for an admin user.")
        return value

    def validate(self, data):
        # Perform object-level validation, specifically checking if passwords match.
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords don't match."})

        # The nested serializer (facility_details) handles its own validation.
        # Its errors will be automatically included if data is invalid.
        return data

    def create(self, validated_data):
        """
        Overrides the create method to handle the creation of both a HealthFacility
        and a User instance from the validated data.
        """
        # Extract nested facility data
        facility_data = validated_data.pop('facility_details')

        # Extract user data
        username = validated_data['username']
        email_admin = validated_data['email_admin']
        password = validated_data['password']

        # 1. Create the HealthFacility
        try:
            health_facility = HealthFacility.objects.create(**facility_data)
        except IntegrityError as e:
            # Catch database-level errors like unique constraints on facility name
            raise serializers.ValidationError({"facility_details": f"Error creating facility: {e}"})

        # 2. Create the User (Facility Admin)
        user = User.objects.create_user(
            username=username,
            email=email_admin,
            password=password,
            is_staff=True,
            is_facility_admin=True, # Assuming this field exists on your CustomUser
            is_active=True,
        )

        # Optional: Link the user to the facility if your models support this
        # e.g., if HealthFacility has a ForeignKey to User for its 'admin'
        # health_facility.admin = user
        # health_facility.save()

        # Or if you have a separate FacilityAdminProfile model:
        # from .models import FacilityAdminProfile
        # FacilityAdminProfile.objects.create(user=user, facility=health_facility)

        return {
            'user': user,
            'health_facility': health_facility
        }
#END


#These serializers are for the Facility admin, They manage everything under here
class FacilityReportSerializer(serializers.ModelSerializer):
    generated_by_name = serializers.CharField(source='generated_by.get_full_name', read_only=True)
    facility_name = serializers.CharField(source='facility.name', read_only=True)
    report_type_display = serializers.CharField(source='get_report_type_display', read_only=True)
    
    class Meta:
        model = FacilityReport
        fields = [
            'id', 'facility', 'facility_name', 'report_type', 'report_type_display',
            'generated_by', 'generated_by_name', 'generated_at', 'report_file',
            'parameters', 'is_downloaded'
        ]
        read_only_fields = ['generated_at', 'generated_by']

    def create(self, validated_data):
        validated_data['generated_by'] = self.context['request'].user
        return super().create(validated_data)

class HealthcareWorkerSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    facility_name = serializers.CharField(source='facility.name', read_only=True)
    position_display = serializers.CharField(source='get_position_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = HealthcareW
        fields = [
            'worker_id', 'username', 'first_name', 'last_name', 'full_name',
            'email', 'phone_number', 'position', 'position_display',
            'facility', 'facility_name', 'Facility_admin', 'temporary_password',
            'password_changed', 'status', 'status_display', 'date_joined',
            'date_left', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'date_joined']
        extra_kwargs = {
            'temporary_password': {'write_only': True},
        }

    def validate_worker_id(self, value):
        if len(value) > 15:
            raise serializers.ValidationError("Worker ID cannot exceed 15 characters.")
        return value

    def validate_email(self, value):
        if value and HealthcareW.objects.filter(email=value).exclude(
            worker_id=self.instance.worker_id if self.instance else None
        ).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

class HealthcareWorkerCreateSerializer(serializers.ModelSerializer):
    #Separate serializer for creating healthcare workers
    
    class Meta:
        model = HealthcareW
        fields = [
            'worker_id', 'username', 'first_name', 'last_name', 'email',
            'phone_number', 'position', 'facility', 'Facility_admin',
            'temporary_password', 'status'
        ]

    def validate_worker_id(self, value):
        if HealthcareW.objects.filter(worker_id=value).exists():
            raise serializers.ValidationError("Worker ID already exists.")
        return value

#END


#These serializers are for the Healthcare Worker, everything they manage is here

#This is for the mobile app 
class ChildSerializer(serializers.ModelSerializer):
    age_months = serializers.SerializerMethodField()
    
    class Meta:
        model = Child
        fields = ['id', 'first_name', 'last_name', 'date_of_birth', 'age_months']
    
    def get_age_months(self, obj):
        from datetime import date
        today = date.today()
        age = today - obj.date_of_birth
        return int(age.days / 30.44)  # approximate months

class VaccinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaccinationRecord
        fields = '__all__'

class GrowthRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrowthRecord
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
#END