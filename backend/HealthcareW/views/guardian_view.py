from rest_framework.views import APIView
from api.myserializers.guardian_serializer import CreateGuardianSerializer, UpdateGuardianSerializer, ListGuardianSerializer
from HealthcareW.models import Guardian
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from HealthcareW.views.permissions_view import IsHealthcareWorker

# View for creating a new Guardian
class CreateGuardian(APIView):
    permission_classes = [IsAuthenticated, IsHealthcareWorker]  # Ensure the user is authenticated and is a healthcare worker
    def post(self, request, *args, **kwargs):
        serializer = CreateGuardianSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid(): 
            serializer.save()

            return Response({"message": "Guardian Creation Successful", "data": serializer.data,
                             "status": status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)

        return Response({"message": "Guardian Creation Failed", "errors": serializer.errors,
                         "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    
# View for updating an existing Guardian
class UpdateGuardian(APIView):
    permission_classes = [IsAuthenticated, IsHealthcareWorker]  # Ensure the user is authenticated and is a healthcare worker
    def put(self, request, *args, **kwargs):
        national_id = kwargs.get('national_id')
        try:
            guardian = Guardian.objects.get(national_id=national_id)
        except Guardian.DoesNotExist:
            return Response({"message": "Guardian not found", "status": status.HTTP_404_NOT_FOUND}, 
                            status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateGuardianSerializer(guardian, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Guardian Update Successful", "data": serializer.data,
                             "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)

        return Response({"message": "Guardian Update Failed", "errors": serializer.errors,
                         "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
# View for listing all Guardians
class ListGuardian(APIView):
    permission_classes = [IsAuthenticated, IsHealthcareWorker]  # Ensure the user is authenticated and is a healthcare worker
    def get(self, request):
        guardians = Guardian.objects.all()
        serializer = ListGuardianSerializer(guardians, many=True)

        return Response({"message": "Guardian List Retrieved Successfully", "data": serializer.data,
                         "status": status.HTTP_200_OK})
    
class DeleteGuardian(APIView):
    permission_classes = [IsAuthenticated, IsHealthcareWorker]  # Ensure the user is authenticated and is a healthcare worker
    def delete(self, request, national_id, *args, **kwargs):
        try:
            guardian = Guardian.objects.get(national_id=national_id)
            guardian.delete()
            return Response({"message": "Guardian deleted successfully", "status": status.HTTP_204_NO_CONTENT}, 
                            status=status.HTTP_204_NO_CONTENT)
        except Guardian.DoesNotExist:
            return Response({"message": "Guardian not found", "status": status.HTTP_404_NOT_FOUND}, 
                            status=status.HTTP_404_NOT_FOUND)