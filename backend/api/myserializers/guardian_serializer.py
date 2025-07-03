from rest_framework import serializers
from HealthcareW.models import Guardian

# Serializer for creating a new guardian instance
class CreateGuardianSerializer(serializers.Serializer):
    national_id = serializers.CharField(max_length=20, unique=True)
    fullname = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=15, required=False, allow_blank=True)

    def create(self, validated_data):
        national_id = validated_data.pop('national_id')
        fullname = validated_data.pop('fullname')
        email = validated_data.pop('email')
        phone_number = validated_data.pop('phone_number')

        guardian = Guardian(national_id=national_id, fullname=fullname,
                            email=email, phone_number=phone_number)
        guardian.save()
        return guardian
    
# Serializer for updating an existing guardian instance
class UpdateGuardianSerializer(serializers.Serializer):
   
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=15, required=False, allow_blank=True)

    def update(self, instance, validated_data):
        
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()
        return instance
    
# Serializer for listing all guardian instances
class ListGuardianSerializer(serializers.Serializer):
    national_id = serializers.CharField(max_length=20, unique=True)
    fullname = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=15, required=False, allow_blank=True)
    
    