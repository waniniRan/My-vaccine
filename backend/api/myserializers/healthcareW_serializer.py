from rest_framework import serializers
from Facilityadmin.models.HealthcareW import HealthcareW
from Sysadmin.models.User import User
from Sysadmin.models.HealthFacility import HealthFacility

# Serializer to create a new healthcare worker instance
class CreateHealthcareWSerializer(serializers.Serializer):
    facility = serializers.CharField(max_length=150, required=True)
    worker_username= serializers.CharField(max_length=150)
    email = serializers.EmailField(required=False)
    fullname= serializers.CharField(max_length=120)
    phone_number= serializers.CharField(max_length=15, required=False)
    position= serializers.CharField(max_length=20)
    temporary_password = serializers.CharField(write_only=True)
    status= serializers.CharField(max_length=10)

    def create(self, validated_data):
        facility_id = validated_data.pop('facility')
        worker_username = validated_data.pop('worker_username')
        fullname = validated_data.pop('fullname')
        email = validated_data.pop('email', None)
        phone_number = validated_data.pop('phone_number', None)
        position = validated_data.pop('position')
        temporary_password = validated_data.pop('temporary_password')
        status = validated_data.pop('status')

        # Check if username is taken
        if User.objects.filter(username=worker_username).exists():
            raise serializers.ValidationError({"worker_username": "This username is already taken."})

        # get the facility
        try:
            facility = HealthFacility.objects.get(ID=facility_id)
        except HealthFacility.DoesNotExist:
            raise serializers.ValidationError({"facility": "Facility not found."})

        # create the related user account
        user = User.objects.create_user(
            username=worker_username,
            email=email,
            password=temporary_password,
            role=User.Role.WORKER,
            must_change_password=True
        )

        healthcare_worker = HealthcareW(
            user=user,
            worker_username=worker_username,
            fullname=fullname,
            email=email,
            phone_number=phone_number,
            position=position,
            facility=facility,
            Facility_admin=self.context['request'].user.facility_admin,
            temporary_password=temporary_password,
            status=status,
            password_changed=False
        )
        healthcare_worker.save()
        return healthcare_worker

    
# Serializer to update an existing healthcare worker instance
class UpdateHealthcareWSerializer(serializers.Serializer):
    
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=15, required=False)
    status = serializers.CharField(max_length=10)
   
    def update(self, instance, validated_data):
        
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
    
# Serializer for listing healthcare worker instances
class ListHealthcareWSerializer(serializers.Serializer):

    worker_id = serializers.CharField(max_length=15)
    worker_username = serializers.CharField(max_length=20)
    fullname= serializers.CharField(max_length=200)
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(max_length=15, required=False)
    position = serializers.CharField(max_length=20)
    facility = serializers.CharField(source='facility.name', read_only=True)
    status = serializers.CharField(max_length=10)
