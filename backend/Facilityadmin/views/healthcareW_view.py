from rest_framework.views import APIView
from api.myserializers.healthcareW_serializer import CreateHealthcareWSerializer, UpdateHealthcareWSerializer, ListHealthcareWSerializer
from Facilityadmin.models.HealthcareW import HealthcareW
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from Facilityadmin.views.permissions_view import IsFacilityAdmin

# View for creating a new Healthcare Worker
class CreateHealthcareW(APIView):
    permission_classes = [IsFacilityAdmin, IsAuthenticated]
    def post(self, request, *args, **kwargs):
        print("DEBUG: incoming data →", request.data)   # 👈 guaranteed to print
        serializer = CreateHealthcareWSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
           print("DEBUG: valid →", serializer.validated_data)  # 👈
           serializer.save()
           return Response({
            "message": "Healthcare Worker Creation Successful",
            "data": serializer.data,
            "status": status.HTTP_201_CREATED
        }, status=status.HTTP_201_CREATED)
        else:
          print("DEBUG: errors →", serializer.errors)   # 👈
          return Response({
            "message": "Healthcare Worker Creation Failed",
            "errors": serializer.errors,
            "status": status.HTTP_400_BAD_REQUEST
        }, status=status.HTTP_400_BAD_REQUEST)

    
# View for updating an existing Healthcare Worker
class UpdateHealthcareW(APIView):
    permission_classes = [IsFacilityAdmin, IsAuthenticated]
    def put(self, request, *args, **kwargs):
        worker_id = kwargs.get('worker_id')
        try:
            healthcare_worker = HealthcareW.objects.get(worker_id=worker_id)
        except HealthcareW.DoesNotExist:
            return Response({"message": "Healthcare Worker not found", "status": status.HTTP_404_NOT_FOUND}, 
                            status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateHealthcareWSerializer(healthcare_worker, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Healthcare Worker Update Successful", "data": serializer.data,
                             "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)

        return Response({"message": "Healthcare Worker Update Failed", "errors": serializer.errors,
                         "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    
# View for listing all Healthcare Workers
class ListHealthcareW(APIView):
    permission_classes = [IsFacilityAdmin, IsAuthenticated]
    def get(self, request):
        workers = HealthcareW.objects.all()
        if not workers.exists():
            return Response({'data': []}, status=200)
        serializer = ListHealthcareWSerializer(workers, many=True)
        return Response({'data': serializer.data}, status=200)

class DeleteHealthcareW(APIView):
    permission_classes = [IsFacilityAdmin, IsAuthenticated]
    def delete(self, request, worker_id, *args, **kwargs):
        try:
            worker = HealthcareW.objects.get(worker_id=worker_id)
            worker.delete()
            return Response({"message": "Deleted"}, status=status.HTTP_200_OK)
        except HealthcareW.DoesNotExist:
            return Response({"message": "Worker not found"}, status=status.HTTP_404_NOT_FOUND)
