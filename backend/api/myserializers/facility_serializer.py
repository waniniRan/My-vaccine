from rest_framework import serializers
from Sysadmin.models.User import User
from Sysadmin.models.HealthFacility import HealthFacility
from Sysadmin.models.FacilityAdmin import FacilityAdmin

class CreateHealthFacilitySerializer(serializers.Serializer): 
    name = serializers.CharField(max_length=200)
    facility_type = serializers.CharField(max_length=50)
    location = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=20)
    email = serializers.EmailField()
    admin = serializers.IntegerField(required=False, allow_null=True, default=None, help_text="ID of the admin user managing this facility")
    

    def create(self, validated_data):
        name=validated_data.pop('name')
        facility_type =validated_data.pop('facility_type')
        location=validated_data.pop('location')
        phone=validated_data.pop('phone')
        email=validated_data.pop('email')
        admin_id=validated_data.get('admin', None)

        user = self.context['request'].user #System admin creating the facility

        admin = None
        if admin_id:
            try:
                admin = User.objects.get(pk=admin_id)
            except User.DoesNotExist:
                raise serializers.ValidationError({"admin": "Admin user not found."})
    
        #created_by = User.objects.get()
        category = HealthFacility(name=name,admin=admin, facility_type=facility_type, 
                                  location=location, phone=phone, email=email, created_by=user)
        category.save()

        return category
    
#Serializer for updating health facility details
class UpdateHealthFacilitySerializer(serializers.Serializer):
    location = serializers.CharField(max_length=100, required=False)
    phone = serializers.CharField(max_length=20, required=False)
    email = serializers.EmailField(required=False)
    admin = serializers.IntegerField(write_only=True, required=False)

    def update(self, instance, validated_data):
        admin_id = validated_data.pop('admin', None)
        if admin_id:
            try:
                instance.admin = User.objects.get(pk=admin_id)
            except User.DoesNotExist:
                raise serializers.ValidationError({"admin": "Admin user not found."})

        instance.location = validated_data.get('location', instance.location)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.email = validated_data.get('email', instance.email)

        instance.save()
        return instance
   

# Serializer for reading created health facilities
class ListHealthFacilitySerializer(serializers.Serializer):
    ID = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=200)
    facility_type = serializers.CharField(max_length=50)
    location = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=20)
    email = serializers.EmailField()
    admin = serializers.StringRelatedField(source='admin_username', read_only=True)
