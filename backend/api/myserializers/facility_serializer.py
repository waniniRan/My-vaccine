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
    
