# backend/Sysadmin/views/activity_api.py
from rest_framework.views import APIView
from rest_framework.response import Response
from Sysadmin.models.SystemActivityLog import SystemActivityLog
from api.myserializers.activity_serializer import SystemActivityLogSerializer
from Sysadmin.views.permissions import IsSystemAdmin
from rest_framework.permissions import IsAuthenticated

class SystemActivityLogAPIView(APIView):
    permission_classes = [IsSystemAdmin, IsAuthenticated]  # Ensure the user is a system admin

    def get(self, request):
        logs = SystemActivityLog.objects.all()
        serializer = SystemActivityLogSerializer(logs, many=True)
        return Response(serializer.data)