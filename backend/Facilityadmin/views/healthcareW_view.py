from rest_framework.views import APIView
from api.myserializers.healthcareW_serializer import CreateHealthcareWSerializer, UpdateHealthcareWSerializer, ListHealthcareWSerializer
from Facilityadmin.models import HealthcareW
from rest_framework.response import Response
from rest_framework import status

# View for creating a new Healthcare Worker
class CreateHealthcareW(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CreateHealthcareWSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid(): 
            serializer.save()

            return Response({"message": "Healthcare Worker Creation Successful", "data": serializer.data,
                             "status": status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)

        return Response({"message": "Healthcare Worker Creation Failed", "errors": serializer.errors,
                         "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    
# View for updating an existing Healthcare Worker
class UpdateHealthcareW(APIView):
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
    def get(self, request):
        healthcare_workers = HealthcareW.objects.all()
        serializer = ListHealthcareWSerializer(healthcare_workers, many=True)

        return Response({"message": "Healthcare Worker List Retrieved Successfully", "data": serializer.data,
                         "status": status.HTTP_200_OK})
