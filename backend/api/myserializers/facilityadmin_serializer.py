from rest_framework import serializers
from Sysadmin.models import User, FacilityAdmin

#Serializer for creation of Facility admin
class CreateFacilityAdminSerializer(serializers.Serializer):
    facility = serializers.CharField(max_length=150, required=True)
    admin_id = serializers.CharField(max_length=15, unique=True, editable=False)
    admin_username= serializers.CharField(max_length=150, unique=True)
    email = serializers.EmailField(required=True)
    fullname= serializers.CharField(max_length=120)

    def create(self, validated_data):
        facility = validated_data.pop('facility')
        admin_id = validated_data.pop('admin_id')
        admin_username = validated_data.pop('admin_username')
        fullname = validated_data.pop('fullname')
        email = validated_data.pop('email')

        facility_admin = FacilityAdmin(facility=facility,
                                       admin_id=admin_id, admin_username=admin_username,
                                       email=email, fullname=fullname)
        facility_admin.save()
        return facility_admin
    
#Serializer for updating Facility admin
class UpdateFacilityAdminSerializer(serializers.Serializer):
    
    email = serializers.EmailField(required=True)

    def update(self, instance, validated_data):
        
        instance.email = validated_data.get('email', instance.email)
       
        instance.save()
        return instance
    
#Serializer for listing Facility admin
class ListFacilityAdminSerializer(serializers.Serializer):
    facility = serializers.CharField(max_length=150, required=True)
    admin_id = serializers.CharField(max_length=15, unique=True, editable=False)
    admin_username= serializers.CharField(max_length=150, unique=True)
    fullname= serializers.CharField(max_length=120)
    email = serializers.EmailField(required=True)
    is_active = serializers.BooleanField(default=True)
    updated_at = serializers.DateTimeField(auto_now=True)

   #def to_representation(self, instance):
     