from rest_framework import serializers
from HealthcareW.models import Notification, Guardian

# Serializer for creation of a new notification instance
class CreateNotificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    notification_type = serializers.CharField(max_length=20)
    message = serializers.TextField()
    is_sent = serializers.BooleanField(default=False)
    date_sent = serializers.DateTimeField(null=True, blank=True)

    def create(self, validated_data):
        email = validated_data.pop('email')
        notification_type = validated_data.pop('notification_type')
        message = validated_data.pop('message')
        is_sent = validated_data.pop('is_sent')
        date_sent = validated_data.pop('date_sent')
        
        Notification = Notification(email=email, notification_type=notification_type, message=message,
                                is_sent=is_sent, date_sent=date_sent)
        Notification.save()
        return Notification

#Serializer for updating a created instance 
class UpdateNotificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
   

    def update(self, instance, validated_data):
       instance.email = validated_data.get('email', instance.email)
       instance.save()
       return instance

# Serializer for viewing all created instances
class ListNotificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    notification_type = serializers.CharField(max_length=20)
    message = serializers.TextField()
    is_sent = serializers.BooleanField(default=False)
    date_sent = serializers.DateTimeField(null=True, blank=True)
