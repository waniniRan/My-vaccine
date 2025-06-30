from rest_framework import serializers
from Sysadmin.models import User,HealthFacility

class CreateHealthFacilitySerializer(serializers.Serializer): 
    name = serializers.CharField(max_length=200)
    facility_type = serializers.CharField(max_length=50)
    location = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=20)
    email = serializers.EmailField()
    admin = serializers.IntegerField(write_only=True)
    

    def create(self, validated_data):
        name=validated_data.pop('name')
        facility_type =validated_data.pop('facility_type')
        location=validated_data.pop('location')
        phone=validated_data.pop('phone')
        email=validated_data.pop('email')
        admin=validated_data.pop('admin')
        admin = User.objects.get(pk=admin)
        #created_by = User.objects.get()
        category = HealthFacility(name=name, admin=admin, facility_type=facility_type, 
                                  location=location, phone=phone, email=email, created_by=admin)
        category.save()

        return category
    
#Serializer for updating health facility details
class UpdateHealthFacilitySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200, required=False)
    facility_type = serializers.CharField(max_length=50, required=False)
    location = serializers.CharField(max_length=100, required=False)
    phone = serializers.CharField(max_length=20, required=False)
    email = serializers.EmailField(required=False)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.facility_type = validated_data.get('facility_type', instance.facility_type)
        instance.location = validated_data.get('location', instance.location)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance    

# Serializer for reading created health facilities
class ListHealthFacilitySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=200)
    facility_type = serializers.CharField(max_length=50)
    location = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=20)
    email = serializers.EmailField()
    admin = serializers.StringRelatedField(source='admin.username', read_only=True)
