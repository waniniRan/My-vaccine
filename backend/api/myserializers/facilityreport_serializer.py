from rest_framework import serializers
from Facilityadmin.models.FacilityReport import FacilityReport

class FacilityReportSerializer(serializers.Serializer):
    generated_by = serializers.DateTimeField()
    facility = serializers.CharField(max_length=150)

    class Meta:
        model = FacilityReport
        fields = '__all__'
