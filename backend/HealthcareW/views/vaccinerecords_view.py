from rest_framework.views import APIView
from api.myserializers.vaccinationrecord_serializer import CreateVaccinationRecordSerializer, UpdateVaccinationRecordSerializer, ListVaccinationRecordSerializer
from HealthcareW.models import VaccinationRecord # Assuming VaccinationRecord is the model for vaccination records
from rest_framework.response import Response
from rest_framework import status

# View to create a new vaccination record instance
class CreateVaccinationRecord(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CreateVaccinationRecordSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid(): 
            serializer.save()

            return Response({"message": "Vaccination Record Creation Successful", "data": serializer.data,
                             "status": status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)

        return Response({"message": "Vaccination Record Creation Failed", "errors": serializer.errors,
                         "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    
# View for updating an existing vaccination record
class UpdateVaccinationRecord(APIView):
    def put(self, request, *args, **kwargs):
        recordID = kwargs.get('recordID')
        try:
            record = VaccinationRecord.objects.get(id=recordID)
        except VaccinationRecord.DoesNotExist:
            return Response({"message": "Vaccination Record not found", "status": status.HTTP_404_NOT_FOUND}, 
                            status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateVaccinationRecordSerializer(record, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Vaccination Record Update Successful", "data": serializer.data,
                             "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)

        return Response({"message": "Vaccination Record Update Failed", "errors": serializer.errors,
                         "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

# View for listing all vaccination records
class ListVaccinationRecord(APIView):
    def get(self, request):
        records = VaccinationRecord.objects.all()
        serializer = ListVaccinationRecordSerializer(records, many=True)

        return Response({"message": "Vaccination Record List Retrieved Successfully", "data": serializer.data,
                         "status": status.HTTP_200_OK})
