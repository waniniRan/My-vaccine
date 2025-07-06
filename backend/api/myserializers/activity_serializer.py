# backend/Sysadmin/serializers/activity_serializers.py
from rest_framework import serializers
from Sysadmin.models.SystemActivityLog import SystemActivityLog

class SystemActivityLogSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    admin = serializers.CharField()
    action = serializers.CharField()
    target_type = serializers.CharField()
    target_id = serializers.CharField()
    description = serializers.CharField()
    timestamp = serializers.DateTimeField()
    ip_address = serializers.CharField(allow_null=True)