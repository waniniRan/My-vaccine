# backend/Sysadmin/views/activity_api.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from Sysadmin.models.SystemActivityLog import SystemActivityLog
from api.myserializers.activity_serializer import SystemActivityLogSerializer

class SystemActivityLogAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        logs = SystemActivityLog.objects.all()
        serializer = SystemActivityLogSerializer(logs, many=True)
        return Response(serializer.data)