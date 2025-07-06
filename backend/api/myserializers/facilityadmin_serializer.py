from rest_framework import serializers
from Sysadmin.models.User import User
from Sysadmin.models.FacilityAdmin import FacilityAdmin
from Sysadmin.models.HealthFacility import HealthFacility

class CreateFacilityAdminSerializer(serializers.Serializer):
    facility = serializers.CharField(max_length=150, required=True)
    admin_username= serializers.CharField(max_length=150)
    email = serializers.EmailField(required=True)
    fullname= serializers.CharField(max_length=120)
    temporary_password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        facility_id = validated_data.pop('facility')
        admin_username = validated_data.pop('admin_username')
        fullname = validated_data.pop('fullname')
        email = validated_data.pop('email')
        temporary_password = validated_data.pop('temporary_password')

        # Check if username is already taken
        if User.objects.filter(username=admin_username).exists():
            raise serializers.ValidationError({"admin_username": "This username is already taken. Please choose another."})

        # get the facility object
        try:
            facility = HealthFacility.objects.get(ID=facility_id)
        except HealthFacility.DoesNotExist:
            raise serializers.ValidationError({"facility": "Facility not found"})

        # check if there is already a facility admin
        if FacilityAdmin.objects.filter(facility=facility).exists():
            raise serializers.ValidationError({"facility": "This facility already has an admin."})

        # create the related user account
        user = User.objects.create_user(
            username=admin_username,
            email=email,
            password=temporary_password,
            role=User.Role.FACILITY_ADMIN,
            must_change_password=True
        )

        facility_admin = FacilityAdmin(
            user=user,
            fullname=fullname,
            email=email,
            facility=facility,
            admin_username=admin_username,
            temporary_password=temporary_password,
            is_active=True
        )
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
    facility = serializers.CharField(source='facility.name', read_only=True)
    admin_id = serializers.CharField(max_length=15)
    admin_username= serializers.CharField(max_length=150)
    fullname= serializers.CharField(max_length=120)
    email = serializers.EmailField(required=True)
    is_active = serializers.BooleanField(default=True)
    updated_at = serializers.DateTimeField()

   #def to_representation(self, instance):
     