from rest_framework import serializers
from HealthcareW.models.Child import Child
from HealthcareW.models.Guardian import Guardian
from datetime import date

# Serializer to create a new child instance
class CreateChildSerializer(serializers.Serializer):
    child_id = serializers.CharField(max_length=20, required=False, read_only=True)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    date_of_birth = serializers.DateField()
    gender = serializers.CharField(max_length=10)
    birth_weight = serializers.DecimalField(max_digits=5, decimal_places=2)
    birth_height = serializers.DecimalField(max_digits=5, decimal_places=2)
    national_id = serializers.CharField(max_length=20, write_only=True)

    def create(self, validated_data):
        national_id = validated_data.pop('national_id')
        guardian = Guardian.objects.get(national_id=national_id)
        child = Child.objects.create(guardian=guardian, **validated_data)
        return child

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
    child_id = serializers.CharField(read_only=True)
    full_name = serializers.SerializerMethodField()
    date_of_birth = serializers.DateField()
    gender = serializers.CharField(max_length=10)
    age = serializers.SerializerMethodField()
    guardian_national_id = serializers.CharField(source='guardian.national_id', read_only=True)

    def get_age(self, obj):
        today = date.today()
        return today.year - obj.date_of_birth.year - ((today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day))

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

class GuardianChildSerializer(serializers.Serializer):
    child_id = serializers.CharField(read_only=True)
    full_name = serializers.SerializerMethodField()
    date_of_birth = serializers.DateField()
    gender = serializers.CharField(max_length=10)
    age = serializers.SerializerMethodField()
    birth_weight = serializers.DecimalField(max_digits=5, decimal_places=2)
    birth_height = serializers.DecimalField(max_digits=5, decimal_places=2)

    def get_age(self, obj):
        today = date.today()
        return today.year - obj.date_of_birth.year - ((today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day))

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
