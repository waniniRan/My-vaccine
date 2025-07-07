from rest_framework.views import APIView
from Facilityadmin.models.FacilityReport import FacilityReport
from api.myserializers.facilityreport_serializer import FacilityReportSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status   

class ListFacilityReports(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reports = FacilityReport.objects.all()
        serializer = FacilityReportSerializer(reports, many=True)
        return Response(serializer.data)

class UploadFacilityReport(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FacilityReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
