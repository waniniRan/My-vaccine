from rest_framework import serializers
from HealthcareW.models.GrowthRecord import GrowthRecord
from HealthcareW.models.Child import Child
from datetime import date

# Serializer for creating a new growth record instance
class CreateGrowthRecordSerializer(serializers.Serializer):
    child_id = serializers.CharField(max_length=20, write_only=True)
    weight = serializers.DecimalField(max_digits=5, decimal_places=2)
    height = serializers.DecimalField(max_digits=5, decimal_places=2)
    date_recorded = serializers.DateField()
    notes = serializers.CharField(allow_blank=True, required=False)
    recorded_by = serializers.CharField(max_length=50, write_only=True)

    def create(self, validated_data):
        child_id = validated_data.pop('child_id')
        child = Child.objects.get(child_id=child_id)
        growth_record = GrowthRecord.objects.create(child=child, **validated_data)
        return growth_record

# Serializer for updating an existing growth record instance
class UpdateGrowthRecordSerializer(serializers.Serializer):
    weight = serializers.DecimalField(max_digits=5, decimal_places=2, help_text="Weight in kg")
    height = serializers.DecimalField(max_digits=5, decimal_places=2, help_text="Height in cm")
    notes = serializers.CharField(allow_blank=True, required=False)

    def update(self, instance, validated_data):
        instance.weight = validated_data.get('weight', instance.weight)
        instance.height = validated_data.get('height', instance.height)
        instance.notes = validated_data.get('notes', instance.notes)
        instance.save()
        return instance
    
# Serializer for listing all growth record instances
class ListGrowthRecordSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    child_id = serializers.CharField(source='child.child_id', read_only=True)
    weight = serializers.DecimalField(max_digits=5, decimal_places=2)
    height = serializers.DecimalField(max_digits=5, decimal_places=2)
    date_recorded = serializers.DateField()
    notes = serializers.CharField(allow_blank=True, required=False)
    recorded_by = serializers.CharField(max_length=50, read_only=True)

class GuardianGrowthRecordSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    weight = serializers.DecimalField(max_digits=5, decimal_places=2)
    height = serializers.DecimalField(max_digits=5, decimal_places=2)
    date_recorded = serializers.DateField()
    notes = serializers.CharField(allow_blank=True, required=False)
    bmi = serializers.SerializerMethodField()

    def get_bmi(self, obj):
        try:
            height_m = obj.height / 100.0
            return round(obj.weight / (height_m * height_m), 2) if height_m > 0 else None
        except Exception:
            return None