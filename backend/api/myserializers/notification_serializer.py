from rest_framework import serializers
from HealthcareW.models import Notification, Guardian

# Serializer for creation of a new notification instance
class CreateNotificationSerializer(serializers.Serializer):
    notification_type = serializers.CharField(max_length=20)
    message = serializers.CharField(max_length=500)
    is_sent = serializers.BooleanField(default=False)
    date_sent = serializers.DateTimeField()

    guardian_email = serializers.EmailField(source='guardian.email',read_only=True)

    def get_guardian_email(self, obj):
        return obj.guardian.email if obj.guardian else None
    def create_email(self, validated_data):
        request = self.context.get('request')
        guardian=request.user.Guardian
        return Notification.objects.create(guardian=guardian, **validated_data)

    def create(self, validated_data):
        notification_type = validated_data.pop('notification_type')
        message = validated_data.pop('message')
        is_sent = validated_data.pop('is_sent')
        date_sent = validated_data.pop('date_sent')
        
        Notification = Notification(notification_type=notification_type, message=message,
                                is_sent=is_sent, date_sent=date_sent)
        Notification.save()
        return Notification

#Serializer for updating a created instance 
class UpdateNotificationSerializer(serializers.Serializer):
    guardian_email = serializers.EmailField()
   

    def update(self, instance, validated_data):
       instance.email = validated_data.get('email', instance.email)
       instance.save()
       return instance

# Serializer for viewing all created instances
class ListNotificationSerializer(serializers.Serializer):
    guardian_email = serializers.EmailField(source='guardian.email', read_only=True)
    notification_type = serializers.CharField(max_length=20)
    message = serializers.CharField(max_length=500)
    is_sent = serializers.BooleanField(default=False)
    date_sent = serializers.DateTimeField()
