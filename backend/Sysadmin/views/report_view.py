# backend/Sysadmin/views/report_api.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.conf import settings
from rest_framework import status
from Sysadmin.models.SystemReport import SystemReport
from api.myserializers.report_serializer import SystemReportListSerializer

class SystemReportsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        reports = SystemReport.objects.all()
        serializer = SystemReportListSerializer(reports, many=True)
        return Response({"message": "Reports loaded successfully",
            "data": serializer.data,
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)

        