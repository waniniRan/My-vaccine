from rest_framework import serializers
from HealthcareW.models import GrowthRecord, Child

# Serializer for creating a new growth record instance
class CreateGrowthRecordSerializer(serializers.Serializer):
    child_id = serializers.CharField(Child)
    weight = serializers.DecimalField(max_digits=5, decimal_places=2, help_text="Weight in kg")
    height = serializers.DecimalField(max_digits=5, decimal_places=2, help_text="Height in cm")
    recorded_by = serializers.CharField('Facilityadmin.HealthcareW')
    date_recorded = serializers.DateField()
    notes = serializers.CharField(max_length=300)

    def create(self, validated_data):
        child_id = validated_data.pop('child_id')
        weight = validated_data.pop('weight')
        height = validated_data.pop('height')
        recorded_by = validated_data.pop('recorded_by')
        date_recorded = validated_data.pop('date_recorded')
        notes = validated_data.pop('notes')

        growth_record = GrowthRecord(child_id=child_id, weight=weight, height=height,
                                     recorded_by=recorded_by,
                                     date_recorded=date_recorded, notes=notes)
        growth_record.save()
        return growth_record

# Serializer for updating an existing growth record instance
class UpdateGrowthRecordSerializer(serializers.Serializer):
    
    weight = serializers.DecimalField(max_digits=5, decimal_places=2, help_text="Weight in kg")
    height = serializers.DecimalField(max_digits=5, decimal_places=2, help_text="Height in cm")
    notes = serializers.CharField(blank=True)

    def update(self, instance, validated_data):
       
        instance.weight = validated_data.get('weight', instance.weight)
        instance.height = validated_data.get('height', instance.height)
        instance.notes = validated_data.get('notes', instance.notes)
        instance.save()
        return instance
    
# Serializer for listing all growth record instances
class ListGrowthRecordSerializer(serializers.Serializer):
    child_id = serializers.CharField(Child)
    weight = serializers.DecimalField(max_digits=5, decimal_places=2, help_text="Weight in kg")
    height = serializers.DecimalField(max_digits=5, decimal_places=2, help_text="Height in cm")
    recorded_by = serializers.CharField('Facilityadmin.HealthcareW')
    date_recorded = serializers.DateField()
    notes = serializers.CharField(max_length=300)