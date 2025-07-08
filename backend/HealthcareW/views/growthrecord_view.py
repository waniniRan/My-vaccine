from rest_framework.views import APIView
from api.myserializers.growthrecord_serializer import CreateGrowthRecordSerializer
from api.myserializers.growthrecord_serializer import UpdateGrowthRecordSerializer, ListGrowthRecordSerializer
from HealthcareW.models import GrowthRecord
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from HealthcareW.views.permissions_view import IsHealthcareWorker

# View to create a new growth record instance
class CreateGrowthRecord(APIView):
    permission_classes = [IsHealthcareWorker,IsAuthenticated]  # Ensure the user is authenticated
    def post(self, request, *args, **kwargs):
        serializer = CreateGrowthRecordSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid(): 
            serializer.save()

            return Response({"message": "Growth Record Creation Successful", "data": serializer.data,
                             "status": status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)

        return Response({"message": "Growth Record Creation Failed", "errors": serializer.errors,
                         "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    
# View for updating an existing growth record
class UpdateGrowthRecord(APIView):
    permission_classes = [IsHealthcareWorker,IsAuthenticated]  # Ensure the user is authenticated
    def put(self, request, *args, **kwargs):
        recordID = kwargs.get('recordID')
        try:
            record = GrowthRecord.objects.get(id=recordID)
        except GrowthRecord.DoesNotExist:
            return Response({"message": "Growth Record not found", "status": status.HTTP_404_NOT_FOUND}, 
                            status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateGrowthRecordSerializer(record, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Growth Record Update Successful", "data": serializer.data,
                             "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)

        return Response({"message": "Growth Record Update Failed", "errors": serializer.errors,
                         "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    
# View for listing all growth records
class ListGrowthRecord(APIView):
    permission_classes = [IsHealthcareWorker,IsAuthenticated]  # Ensure the user is authenticated
    def get(self, request):
        records = GrowthRecord.objects.all()
        serializer = ListGrowthRecordSerializer(records, many=True)

        return Response({"message": "Growth Record List Retrieved Successfully", "data": serializer.data,
                         "status": status.HTTP_200_OK})

class DeleteGrowthRecord(APIView):
    permission_classes = [IsHealthcareWorker ,IsAuthenticated]  # Ensure the user is authenticated
    def delete(self, request, recordID, *args, **kwargs):
        try:
            record = GrowthRecord.objects.get(id=recordID)
            record.delete()
            return Response({"message": "Growth Record Deleted Successfully", "status": status.HTTP_204_NO_CONTENT},
                            status=status.HTTP_204_NO_CONTENT)
        except GrowthRecord.DoesNotExist:
            return Response({"message": "Growth Record not found", "status": status.HTTP_404_NOT_FOUND},
                            status=status.HTTP_404_NOT_FOUND)