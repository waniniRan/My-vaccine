from rest_framework.views import APIView
from api.myserializers.facilityadmin_serializer import CreateFacilityAdminSerializer, UpdateFacilityAdminSerializer, ListFacilityAdminSerializer
from Sysadmin.models.FacilityAdmin import FacilityAdmin
from rest_framework.response import Response
from rest_framework import status
from Sysadmin.views.permissions import IsSystemAdmin,IsSystemAdminOrOwner,CanManageFacilities,CanManageUsers
from rest_framework.permissions import IsAuthenticated
# View for creating a new Facility Admin
class CreateFacilityAdmin(APIView):

    permission_classes = [IsAuthenticated,IsSystemAdmin]   # Adjust permissions as needed
    def post(self, request, *args, **kwargs):
        serializer = CreateFacilityAdminSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid(): 
            serializer.save()

            return Response({"message": "Facility Admin Creation Successful", "data": serializer.data,
                             "status": status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)

        return Response({"message": "Facility Admin Creation Failed", "errors": serializer.errors,
                         "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    
# View for updating an existing Facility Admin
class UpdateFacilityAdmin(APIView):
    def put(self, request, *args, **kwargs):
        admin_id = kwargs.get('admin_id')
        try:
            facility_admin = FacilityAdmin.objects.get(admin_id=admin_id)
        except FacilityAdmin.DoesNotExist:
            return Response({"message": "Facility Admin not found", "status": status.HTTP_404_NOT_FOUND}, 
                            status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateFacilityAdminSerializer(facility_admin, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Facility Admin Update Successful", "data": serializer.data,
                             "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)

        return Response({"message": "Facility Admin Update Failed", "errors": serializer.errors,
                         "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    
# View for listing all Facility Admins
class ListFacilityAdmin(APIView):
    def get(self, request):
        facility_admins = FacilityAdmin.objects.all()
        serializer = ListFacilityAdminSerializer(facility_admins, many=True)

        return Response({"message": "Facility Admin List Retrieved Successfully", "data": serializer.data,
                         "status": status.HTTP_200_OK})

class DeleteFacilityAdmin(APIView):
    def delete(self, request, admin_id, *args, **kwargs):
        try:
            admin = FacilityAdmin.objects.get(admin_id=admin_id)
            admin.delete()
            return Response({
                "message": "Facility Admin deleted successfully",
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except FacilityAdmin.DoesNotExist:
            return Response({
                "message": "Facility Admin not found",
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

