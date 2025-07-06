# backend/Sysadmin/serializers/user_serializers.py
from rest_framework import serializers
from Sysadmin.models.User import User


class UserListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.EmailField()
    role = serializers.CharField()