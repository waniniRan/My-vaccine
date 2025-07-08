from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import FileResponse, Http404
from Sysadmin.models.SystemReport import SystemReport
from Sysadmin.views.permissions import IsSystemAdmin
import os

class ReportDownloadView(APIView):
    permission_classes = [IsAuthenticated, IsSystemAdmin]

    def get(self, request, report_id):
        try:
            report = SystemReport.objects.get(id=report_id)
            if not report.report_file:
                return Response({'detail': 'File not found.'}, status=status.HTTP_404_NOT_FOUND)
            file_path = report.report_file.path
            if not os.path.exists(file_path):
                return Response({'detail': 'File does not exist.'}, status=status.HTTP_404_NOT_FOUND)
            response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
            return response
        except SystemReport.DoesNotExist:
            return Response({'detail': 'Report not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 