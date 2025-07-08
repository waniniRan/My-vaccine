from rest_framework.views import APIView
from Facilityadmin.models.FacilityReport import FacilityReport
from api.myserializers.facilityreport_serializer import FacilityReportSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status   
from Facilityadmin.views.permissions_view import IsFacilityAdmin


class ListFacilityReports(APIView):
    permission_classes = [IsFacilityAdmin, IsAuthenticated]

    def get(self, request):
        reports = FacilityReport.objects.all()
        if not reports.exists():
            return Response({'data': []}, status=200)
        serializer = FacilityReportSerializer(reports, many=True)
        return Response({'data': serializer.data}, status=200)

class UploadFacilityReport(APIView):
    permission_classes = [IsFacilityAdmin, IsAuthenticated]

    def post(self, request):
        serializer = FacilityReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'message': 'Facility report uploaded successfully.'}, status=201)
        return Response({'error': serializer.errors}, status=400)
