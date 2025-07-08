# backend/Sysadmin/views/report_api.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status
from Sysadmin.models.SystemReport import SystemReport
from api.myserializers.report_serializer import SystemReportListSerializer
from Sysadmin.views.permissions import IsSystemAdmin
from rest_framework.permissions import IsAuthenticated

class SystemReportsView(APIView):
    permission_classes = [ IsAuthenticated, IsSystemAdmin]

    def get(self, request):
        reports = SystemReport.objects.all()
        if not reports.exists():
            return Response({'data': []}, status=200)
        serializer = SystemReportListSerializer(reports, many=True, context={'request': request})
        return Response({'data': serializer.data}, status=200)

        