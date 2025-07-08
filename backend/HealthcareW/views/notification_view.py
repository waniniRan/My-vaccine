from rest_framework.views import APIView
from api.myserializers.notification_serializer import CreateNotificationSerializer, UpdateNotificationSerializer, ListNotificationSerializer
from HealthcareW.models import Notification
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from HealthcareW.views.permissions_view import IsHealthcareWorker


# View to create a new notification instance
class CreateNotification(APIView):
    permission_classes = [IsHealthcareWorker,IsAuthenticated]  # Ensure the user is authenticated
    def post(self, request, *args, **kwargs):
        serializer = CreateNotificationSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid(): 
            serializer.save()

            return Response({"message": "Notification Creation Successful", "data": serializer.data,
                             "status": status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)

        return Response({"message": "Notification Creation Failed", "errors": serializer.errors,
                         "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    
# View for updating an existing notification
class UpdateNotification(APIView):
    permission_classes = [IsHealthcareWorker,IsAuthenticated]  # Ensure the user is authenticated
    def put(self, request, *args, **kwargs):
        id = kwargs.get('id')
        try:
            notification = Notification.objects.get(id=id)
        except Notification.DoesNotExist:
            return Response({"message": "Notification not found", "status": status.HTTP_404_NOT_FOUND}, 
                            status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateNotificationSerializer(notification, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Notification Update Successful", "data": serializer.data,
                             "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)

        return Response({"message": "Notification Update Failed", "errors": serializer.errors,
                         "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

# View for listing all notifications
class ListNotification(APIView):
    permission_classes = [IsHealthcareWorker,IsAuthenticated]  # Ensure the user is authenticated
    def get(self, request):
        notifications = Notification.objects.all()
        serializer = ListNotificationSerializer(notifications, many=True)

        return Response({"message": "Notification List Retrieved Successfully", "data": serializer.data,
                         "status": status.HTTP_200_OK})

class DeleteNotification(APIView):
    permission_classes = [IsHealthcareWorker,IsAuthenticated]  # Ensure the user is authenticated
    def delete(self, request, id, *args, **kwargs):
        try:
            notification = Notification.objects.get(id=id)
            notification.delete()
            return Response({"message": "Notification deleted successfully", "status": status.HTTP_204_NO_CONTENT}, 
                            status=status.HTTP_204_NO_CONTENT)
        except Notification.DoesNotExist:
            return Response({"message": "Notification not found", "status": status.HTTP_404_NOT_FOUND}, 
                            status=status.HTTP_404_NOT_FOUND)