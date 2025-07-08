from rest_framework import serializers
from HealthcareW.models.VaccinationRecord import VaccinationRecord
from HealthcareW.models.Child import Child
from Sysadmin.models.Vaccine import Vaccine
from datetime import date

# Serializer for creating a new instance of a vaccine record
class CreateVaccinationRecordSerializer(serializers.Serializer):
    child_id = serializers.CharField(max_length=20, write_only=True)
    v_ID = serializers.CharField(max_length=20, write_only=True)
    dose_number = serializers.IntegerField()
    administration_date = serializers.DateField()
    side_effects = serializers.CharField(allow_blank=True, required=False)
    remarks = serializers.CharField(allow_blank=True, required=False)
    administered_by = serializers.CharField(max_length=50, write_only=True)

    def create(self, validated_data):
        child_id = validated_data.pop('child_id')
        v_ID = validated_data.pop('v_ID')
        child = Child.objects.get(child_id=child_id)
        vaccine = Vaccine.objects.get(v_ID=v_ID)
        record = VaccinationRecord.objects.create(child=child, vaccine=vaccine, **validated_data)
        return record

# Serializer for Updating created Vaccination Records
class UpdateVaccinationRecordSerializer(serializers.Serializer):
    dose_number = serializers.IntegerField()
    administration_date = serializers.DateField()
    side_effects = serializers.CharField(allow_blank=True, required=False)
    remarks = serializers.CharField(allow_blank=True, required=False)

    def update(self, instance, validated_data):
        instance.dose_number = validated_data.get('dose_number', instance.dose_number)
        instance.administration_date = validated_data.get('administration_date', instance.administration_date)
        instance.side_effects = validated_data.get('side_effects', instance.side_effects)
        instance.remarks = validated_data.get('remarks', instance.remarks)
        instance.save()
        return instance

# Serializer for listing created Vaccination Records
class ListVaccinationRecordSerializer(serializers.Serializer):
    recordID = serializers.IntegerField(read_only=True)
    child_id = serializers.CharField(source='child.child_id', read_only=True)
    v_ID = serializers.CharField(source='vaccine.v_ID', read_only=True)
    vaccine_name = serializers.CharField(source='vaccine.name', read_only=True)
    dose_number = serializers.IntegerField()
    administration_date = serializers.DateField()
    side_effects = serializers.CharField(allow_blank=True, required=False)
    remarks = serializers.CharField(allow_blank=True, required=False)
    administered_by = serializers.CharField(max_length=50, read_only=True)

class GuardianVaccinationRecordSerializer(serializers.Serializer):
    recordID = serializers.IntegerField(read_only=True)
    v_ID = serializers.CharField(source='vaccine.v_ID', read_only=True)
    vaccine_name = serializers.CharField(source='vaccine.name', read_only=True)
    dose_number = serializers.IntegerField()
    administration_date = serializers.DateField()
    side_effects = serializers.CharField(allow_blank=True, required=False)
    remarks = serializers.CharField(allow_blank=True, required=False)

