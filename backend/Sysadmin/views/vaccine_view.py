from rest_framework.views import APIView
from api.myserializers.vaccine_serializer import CreateVaccineSerializer, UpdateVaccineSerializer, ListVaccineSerializer
from Sysadmin.models.Vaccine import Vaccine
from rest_framework.response import Response
from rest_framework import status
from Sysadmin.views.permissions import IsSystemAdmin, IsSystemAdminOrOwner, CanManageFacilities, CanManageUsers 
from rest_framework.permissions import IsAuthenticated
#View for creating a new Vaccine
class CreateVaccine(APIView):
    permission_classes = [IsAuthenticated,IsSystemAdmin]  # Adjust permissions as needed
    def post(self, request, *args, **kwargs):
        serializer = CreateVaccineSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid(): 
            serializer.save()

            return Response({"message": "Vaccine Creation Successful", "data": serializer.data,
                             "status": status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)

        return Response({"message": "Vaccine Creation Failed", "errors": serializer.errors,
                         "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    
#View for updating an existing Vaccine
class UpdateVaccine(APIView):
    def put(self, request, *args, **kwargs):
        v_ID = kwargs.get('v_ID')
        try:
            vaccine = Vaccine.objects.get(v_ID=v_ID)
        except Vaccine.DoesNotExist:
            return Response({"message": "Vaccine not found", "status": status.HTTP_404_NOT_FOUND}, 
                            status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateVaccineSerializer(vaccine, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Vaccine Update Successful", "data": serializer.data,
                             "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)

        return Response({"message": "Vaccine Update Failed", "errors": serializer.errors,
                         "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    
#View for listing all Vaccines
class ListVaccine(APIView):
    def get(self, request):
        
        vaccines = Vaccine.objects.all()
        serializer = ListVaccineSerializer(vaccines, many=True)

        return Response({"message": "Vaccine List Retrieved Successfully", "data": serializer.data,
                         "status": status.HTTP_200_OK})
    
class DeleteVaccine(APIView):
    def delete(self, request, v_ID, *args, **kwargs):
        try:
            vaccine = Vaccine.objects.get(v_ID=v_ID)
            vaccine.delete()
            return Response({
                "message": "Vaccine deleted successfully",
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except Vaccine.DoesNotExist:
            return Response({
                "message": "Vaccine not found",
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)  