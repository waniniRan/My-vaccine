from rest_framework import serializers
from HealthcareW.models import Child, Guardian

# Serializer to create a new child instance
class CreateChildSerializer(serializers.Serializer):
    child_id = serializers.CharField(max_length=20)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    date_of_birth = serializers.DateField()
    gender = serializers.CharField(max_length=1)
    birth_weight = serializers.DecimalField(max_digits=5, decimal_places=2, help_text="Weight in kg")
    birth_height = serializers.DecimalField(max_digits=5, decimal_places=2, help_text="Height in cm")
    national_id = serializers.CharField(Guardian, related_name='children')

    def create(self, validated_data):
        child_id = validated_data.pop('child_id')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        date_of_birth = validated_data.pop('date_of_birth')
        gender = validated_data.pop('gender')
        birth_weight = validated_data.pop('birth_weight')
        birth_height = validated_data.pop('birth_height')
        national_id = validated_data.pop('national_id')

        category = Child(child_id=child_id, first_name=first_name, last_name=last_name, date_of_birth=date_of_birth,
                         gender=gender, birth_weight=birth_weight, birth_height=birth_height, national_id=national_id)
        category.save()
        return category
    
# Serializer to update a created instance
class UpdateChildSerializer(serializers.Serializer):
    birth_weight = serializers.DecimalField(max_digits=5, decimal_places=2, help_text="Weight in kg")
    birth_height = serializers.DecimalField(max_digits=5, decimal_places=2, help_text="Height in cm")
    

    def update(self, instance, validated_data):
        
        instance.birth_weight = validated_data.get('birth_weight', instance.birth_weight)
        instance.birth_height = validated_data.get('birth_height', instance.birth_height)
        
        instance.save()
        return instance
    
# Serializer for listing created child instances
class ListChildSerializer(serializers.Serializer):
    child_id = serializers.CharField(max_length=20)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    date_of_birth = serializers.DateField()
    gender = serializers.CharField(max_length=1)
    birth_weight = serializers.DecimalField(max_digits=5, decimal_places=2, help_text="Weight in kg")
    birth_height = serializers.DecimalField(max_digits=5, decimal_places=2, help_text="Height in cm")
    national_id = serializers.CharField(max_length=20, help_text="National ID of the guardian")
