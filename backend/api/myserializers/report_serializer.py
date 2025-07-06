# backend/Sysadmin/serializers/report_serializers.py
from rest_framework import serializers
from Sysadmin.models.SystemReport import SystemReport


class SystemReportListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    report_type = serializers.CharField()
    generated_by = serializers.CharField()
    generated_at = serializers.DateTimeField()
    download_url = serializers.CharField()

    def get_download_url(self, obj):
        if obj.file:
            return obj.file.url
        return None