from rest_framework.views import APIView
from api.myserializers.vaccinationrecord_serializer import CreateVaccinationRecordSerializer, UpdateVaccinationRecordSerializer, ListVaccinationRecordSerializer
from HealthcareW.models import VaccinationRecord # Assuming VaccinationRecord is the model for vaccination records
from rest_framework.response import Response
from rest_framework import status, permissions
from HealthcareW.views.permissions_view import IsHealthcareWorker


# View to create a new vaccination record instance
class CreateVaccinationRecord(APIView):
    permission_classes = [permissions.IsAuthenticated, IsHealthcareWorker]
    def post(self, request):
        serializer = CreateVaccinationRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View for updating an existing vaccination record
class UpdateVaccinationRecord(APIView):
    permission_classes = [permissions.IsAuthenticated, IsHealthcareWorker]
    def put(self, request, recordID):
        try:
            record = VaccinationRecord.objects.get(recordID=recordID)
        except VaccinationRecord.DoesNotExist:
            return Response({'error': 'Vaccination record not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UpdateVaccinationRecordSerializer(record, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View for listing all vaccination records
class ListVaccinationRecord(APIView):
    permission_classes = [permissions.IsAuthenticated, IsHealthcareWorker]
    def get(self, request):
        records = VaccinationRecord.objects.all()
        serializer = ListVaccinationRecordSerializer(records, many=True)
        return Response(serializer.data)

class DeleteVaccinationRecord(APIView):
    permission_classes = [permissions.IsAuthenticated, IsHealthcareWorker]
    def delete(self, request, recordID):
        try:
            record = VaccinationRecord.objects.get(recordID=recordID)
        except VaccinationRecord.DoesNotExist:
            return Response({'error': 'Vaccination record not found.'}, status=status.HTTP_404_NOT_FOUND)
        record.delete()
        return Response({'detail': 'Vaccination record deleted.'}, status=status.HTTP_204_NO_CONTENT)