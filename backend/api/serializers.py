#serializers.py
from rest_framework import serializers
from Sysadmin.models import HealthFacility, Vaccine ,User




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
    admin_username = serializers.CharField(source='admin.username', read_only=True)
    admin_email = serializers.EmailField(source='admin.email', required=False)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = HealthFacility
        fields = [
             'id', 'prefix', 'ID', 'name', 'facility_type', 'location', 
    'phone', 'email', 'admin', 'admin_username', 'admin_email',
    'created_by', 'created_by_username', 'created_at', 'updated_at', 'is_active'
           ]
        
        extra_kwargs = {
            'admin': {'write_only': True},
            'created_by': {'write_only': True}
        }

class FacilityAdminCreationSerializer(serializers.Serializer):
    facility_name = serializers.CharField(max_length=200)
    facility_type = serializers.ChoiceField(choices=HealthFacility.FACILITY_TYPES)
    facility_location = serializers.CharField(max_length=100, required=False)
    facility_phone = serializers.CharField(max_length=20, required=False)
    facility_email = serializers.EmailField(required=False)
    admin_username = serializers.CharField(max_length=150)
    admin_email = serializers.EmailField()
    admin_password = serializers.CharField(write_only=True, min_length=8)

    def validate_admin_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_admin_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

class VaccineSerializer(serializers.ModelSerializer):
    facilities_info = serializers.SerializerMethodField()
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Vaccine
        fields = [
            'id', 'name', 'v_ID', 'description', 'dosage', 
    'diseasePrevented', 'recommended_age', 'facility', 
    'facilities_info', 'created_by', 'created_at', 'is_active'
        ]
        read_only_fields = ('v_ID', 'created_by', 'created_at', 'updated_at')

    def get_facilities_info(self, obj):
        return [{
            'id': f.id,
            'name': f.name,
            'type': f.get_facility_type_display(),
            'location': f.location
        } for f in obj.facilities.all()]
    
