from rest_framework import serializers
from Sysadmin.models import Vaccine

#Create a serializer for the Vaccine model
class CreateVaccineSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    v_ID = serializers.CharField(max_length=10)
    description = serializers.TextField(blank=True)
    dosage = serializers.CharField(max_length=50)  # "2 doses", "Single dose", etc.
    diseasePrevented = serializers.CharField(max_length=100)
    recommended_age= serializers.CharField(max_length=20)

    def create(self, validated_data):
        # Create a new Vaccine instance
        name = validated_data.pop('name')
        v_ID = validated_data.pop('v_ID')
        description = validated_data.pop('description')
        dosage = validated_data.pop('dosage')
        diseasePrevented = validated_data.pop('diseasePrevented')
        recommended_age = validated_data.pop('recommended_age')
        
        Vaccine = Vaccine(name=name, v_ID=v_ID, description=description, 
                          dosage=dosage, diseasePrevented=diseasePrevented, 
                          recommended_age=recommended_age)
        Vaccine.save()
        return Vaccine
    
# Serializer for updating vaccine details
class UpdateVaccineSerializer(serializers.Serializer):
    
    
    description = serializers.TextField(blank=True)
    dosage = serializers.CharField(max_length=50)  # "2 doses", "Single dose", etc.
    

    def update(self, instance, validated_data):
       
        instance.description = validated_data.get('description', instance.description)
        instance.dosage = validated_data.get('dosage', instance.dosage)
        
        instance.save()
        return instance
    
# Serializer for listing created vaccines
class ListVaccineSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    v_ID = serializers.CharField(max_length=10)
    description = serializers.CharField(max_length=500, allow_blank=True)
    dosage = serializers.CharField(max_length=50)  # "2 doses", "Single dose", etc.
    diseasePrevented = serializers.CharField(max_length=100)
    recommended_age = serializers.CharField(max_length=20)
