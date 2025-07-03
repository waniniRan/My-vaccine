from rest_framework import serializers
from HealthcareW.models import VaccinationRecord, Child
from Sysadmin.models import Vaccine

#Serializer for creating a new instance of a vaccine record
class CreateVaccinationRecordSerializer(serializers.Serializer):
    child_id = serializers.CharField(Child)
    v_ID = serializers.CharField(Vaccine)
    administered_by = serializers.CharField('Facilityadmin.HealthcareW')
    side_effects = serializers.TextField(blank=True)
    remarks= serializers.TextField(blank=True)
    doseNumber= serializers.IntegerField()

    def create(self, validated_data):
        
        child_id = validated_data.pop('child_id')
        v_ID = validated_data.pop('v_ID')
        administered_by = validated_data.pop('administered_by')
        side_effects = validated_data.pop('side_effects')
        remarks = validated_data.pop('remarks')
        doseNumber = validated_data.pop('doseNumber')

        VaccinationRecord = VaccinationRecord( child_id=child_id, v_ID=v_ID, 
                                       administered_by=administered_by, side_effects=side_effects,
                                      remarks=remarks, doseNumber=doseNumber)
        VaccinationRecord.save()
        return VaccinationRecord

# Serializer for Updating created Vaccination Records
class UpdateVaccinationRecordSerializer(serializers.Serializer):
   
   
    remarks= serializers.TextField(blank=True)
   

    def update(self, instance, validated_data):
       
        instance.remarks = validated_data.get('remarks', instance.remarks)
       
        instance.save()
        return instance

# Serializer for listing created Vaccination Records
class ListVaccinationRecordSerializer(serializers.Serializer):
    recordID = serializers.CharField(max_length=20, unique=True)
    child_id = serializers.CharField(Child)
    v_ID = serializers.CharField(Vaccine)
    administered_by = serializers.CharField('Facilityadmin.HealthcareW')
    side_effects = serializers.TextField(blank=True)
    administrationDate = serializers.DateTimeField(auto_now_add=True)
    remarks = serializers.TextField(blank=True)
    doseNumber = serializers.IntegerField()                          

