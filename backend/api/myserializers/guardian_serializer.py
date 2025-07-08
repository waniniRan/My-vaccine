from rest_framework import serializers
from HealthcareW.models.Guardian import Guardian
from Sysadmin.models.User import User
from HealthcareW.models.Child import Child
from django.contrib.auth.hashers import make_password
from datetime import date

# Serializer for creating a new guardian instance
class CreateGuardianSerializer(serializers.Serializer):
    national_id = serializers.CharField(max_length=20)
    temporary_password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=20)
    full_name = serializers.CharField(max_length=100)

    def create(self, validated_data):
        temp_password = validated_data.pop('temporary_password')
        user = User.objects.create(
            username=validated_data['national_id'],
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            is_active=True
        )
        user.set_password(temp_password)
        user.save()
        guardian = Guardian.objects.create(user=user, **validated_data)
        return guardian

# Serializer for updating an existing guardian instance
class UpdateGuardianSerializer(serializers.Serializer):
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=15)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()
        return instance

# Serializer for listing all guardian instances
class ListGuardianSerializer(serializers.Serializer):
    national_id = serializers.CharField(read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    phone_number = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(source='user.is_active', read_only=True)
    date_registered = serializers.DateTimeField(source='user.date_joined', read_only=True)
    password_changed = serializers.BooleanField(read_only=True)

class GuardianProfileSerializer(serializers.Serializer):
    national_id = serializers.CharField(read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    phone_number = serializers.CharField(read_only=True)
    password_changed = serializers.BooleanField(read_only=True)

class GuardianChildrenSerializer(serializers.Serializer):
    child_id = serializers.CharField(read_only=True)
    full_name = serializers.SerializerMethodField()
    date_of_birth = serializers.DateField()
    gender = serializers.CharField(max_length=10)
    age = serializers.SerializerMethodField()

    def get_age(self, obj):
        today = date.today()
        return today.year - obj.date_of_birth.year - ((today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day))

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    