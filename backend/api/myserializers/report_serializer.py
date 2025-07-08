# backend/Sysadmin/serializers/report_serializers.py
from rest_framework import serializers
from Sysadmin.models.SystemReport import SystemReport


class SystemReportListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    report_type = serializers.CharField()
    generated_at = serializers.DateTimeField()
    generated_by = serializers.CharField()
    download_url = serializers.SerializerMethodField()

    def get_download_url(self, obj):
        request = self.context.get('request')
        if hasattr(obj, 'report_file') and obj.report_file and hasattr(obj.report_file, 'url'):
            return request.build_absolute_uri(obj.report_file.url)
        return None