from rest_framework import serializers
from Facilityadmin.models import HealthcareW

# Serializer to create a new healthcare worker instance
class CreateHealthcareWSerializer(serializers.Serializer):
    fullname = serializers.CharField(max_length=200)
    email = serializers.EmailField(required=False, allow_blank=True)
    phone_number = serializers.CharField(max_length=15, required=False, allow_blank=True)
    position = serializers.CharField(max_length=20)
    facility = serializers.CharField(max_length=100)

    def create(self, validated_data):
        
        fullname = validated_data.pop('fullname')
        email = validated_data.pop('email', None)
        phone_number = validated_data.pop('phone_number', None)
        position = validated_data.pop('position')
        facility = validated_data.pop('facility')
       
        healthcare_worker = HealthcareW(
            fullname=fullname,
            email=email,
            phone_number=phone_number,
            position=position,
            facility=facility,
        )
        healthcare_worker.save()
        return healthcare_worker
    
# Serializer to update an existing healthcare worker instance
class UpdateHealthcareWSerializer(serializers.Serializer):
    
    email = serializers.EmailField(required=False, allow_blank=True)
    phone_number = serializers.CharField(max_length=15, required=False, allow_blank=True)
   
    def update(self, instance, validated_data):
        
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()
        return instance
    
# Serializer for listing healthcare worker instances
class ListHealthcareWSerializer(serializers.Serializer):
    worker_id = serializers.CharField(max_length=20, unique=True, primary_key=True)
    fullname= serializers.CharField(max_length=200)
    email = serializers.EmailField(required=False, allow_blank=True)
    phone_number = serializers.CharField(max_length=15, required=False, allow_blank=True)
    position = serializers.ChoiceField(choices=HealthcareW.Position_Choice)
    facility = serializers.CharField(max_length=100)
    status = serializers.CharField(max_length=10)
