# backend/Sysadmin/serializers/user_serializers.py
from rest_framework import serializers
from Sysadmin.models.User import User


class UserListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.EmailField()
    role = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        if getattr(obj, 'first_name', '') or getattr(obj, 'last_name', ''):
            return f"{obj.first_name} {obj.last_name}".strip()
        return obj.username