# facilities/serializers.py
from rest_framework import serializers
from Sysadmin.models import HealthFacility, Vaccine
from Sysadmin.models import User

class HealthFacilitySerializer(serializers.ModelSerializer):
    admin_username = serializers.CharField(source='admin.username', read_only=True)
    admin_email = serializers.EmailField(source='admin.email', required=False)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = HealthFacility
        fields = [
            'id', 'name', 'facility_type',
            'admin', 'admin_username', 'admin_email',
            'created_by', 'created_by_username', 'created_at'
        ]
        extra_kwargs = {
            'admin': {'write_only': True},
            'created_by': {'write_only': True}
        }

class FacilityAdminCreationSerializer(serializers.Serializer):
    facility_name = serializers.CharField(max_length=200)
    facility_type = serializers.ChoiceField(choices=HealthFacility.FACILITY_TYPES)
    admin_username = serializers.CharField(max_length=150)
    admin_email = serializers.EmailField()
    admin_password = serializers.CharField(write_only=True)

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

    class Meta:
        model = Vaccine
        fields = [
            'id', 'name',  'description',
            'dosage', 'facilities', 'facilities_info',
            'created_by', 'created_at'
        ]
        read_only_fields = ('created_by', 'created_at')

    def get_facilities_info(self, obj):
        return [{
            'id': f.id,
            'name': f.name,
            'type': f.get_facility_type_display()
        } for f in obj.facilities.all()]