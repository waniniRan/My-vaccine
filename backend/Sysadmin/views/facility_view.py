from rest_framework.views import APIView
from api.myserializers.facility_serializer import CreateHealthFacilitySerializer, UpdateHealthFacilitySerializer, ListHealthFacilitySerializer
from Sysadmin.models.HealthFacility import HealthFacility
from rest_framework.response import Response
from rest_framework import status
from Sysadmin.views.permissions import IsSystemAdmin, IsSystemAdminOrOwner, CanManageFacilities, CanManageUsers   
from rest_framework.permissions import IsAuthenticated

class CreateHealthFacility(APIView):
   permission_classes = [IsAuthenticated,IsSystemAdmin]  # Adjust permissions as needed
   def post(self, request, *args, **kwargs):
      
      print("USER DEBUG:", request.user)
      print("USER IS AUTHENTICATED:", request.user.is_authenticated)
      print("USER ROLE:", getattr(request.user, 'role', None))
      serializer = CreateHealthFacilitySerializer(data=request.data, context={'request': request})
         
      if serializer.is_valid(): 
         serializer.save()

         return Response( {"message": "Health facility Creation Successful", "data": serializer.data,
                         "status": status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)

      return Response({"message": "Health Facility Creation Failed", "errors": serializer.errors,
                         "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)  
   
# View for updating an existing Health Facility
class UpdateHealthFacility(APIView):
   
   def put(self, request, *args, **kwargs):
      ID= kwargs.get('ID')
      try:
         facility = HealthFacility.objects.get(ID=ID)
      except HealthFacility.DoesNotExist:
         return Response({"message": "Health Facility not found", "status": status.HTTP_404_NOT_FOUND}, 
                         status=status.HTTP_404_NOT_FOUND)

      serializer = UpdateHealthFacilitySerializer(facility, data=request.data, partial=True)
         
      if serializer.is_valid():
         serializer.save()
         return Response({"message": "Health Facility Update Successful", "data": serializer.data,
                          "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)

      return Response({"message": "Health Facility Update Failed", "errors": serializer.errors,
                       "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
   
# View for listing all Health Facilities
class ListHealthFacility(APIView):
   def get(self, request):
      facilities = HealthFacility.objects.all()
      serializer = ListHealthFacilitySerializer(facilities, many=True)

      return Response({"message": "Health Facility List Retrieved Successfully", "data": serializer.data,
                       "status": status.HTTP_200_OK})

# View for deleting a facility
class DeleteHealthFacility(APIView):
    def delete(self, request, ID, *args, **kwargs):
        try:
            facility = HealthFacility.objects.get(ID=ID)
            facility.delete()
            return Response({
                "message": "Facility deleted successfully",
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except HealthFacility.DoesNotExist:
            return Response({
                "message": "Facility not found",
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

