from rest_framework.views import APIView
from api.myserializers.child_serializer import CreateChildSerializer, UpdateChildSerializer, ListChildSerializer
from HealthcareW.models.Child import Child 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from HealthcareW.views.permissions_view import IsHealthcareWorker

#View to create a new child instance
class CreateChild(APIView):
     permission_classes = [IsHealthcareWorker,IsAuthenticated]  # Ensure the user is authenticated  
     def post(self, request, *args, **kwargs):
        serializer = CreateChildSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid(): 
            serializer.save()

            return Response({"message": "Child Creation Successful", "data": serializer.data,
                             "status": status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)

        return Response({"message": "Child Creation Failed", "errors": serializer.errors,
                         "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
     
#View for updating an existing Vaccine
class UpdateChild(APIView):
    permission_classes = [IsHealthcareWorker,IsAuthenticated]  # Ensure the user is authenticated
    def put(self, request, *args, **kwargs):
        child_id = kwargs.get('child_id')
        try:
            child = Child.objects.get(id=child_id)
        except Child.DoesNotExist:
            return Response({"message": "Child not found", "status": status.HTTP_404_NOT_FOUND}, 
                            status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateChildSerializer(Child, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Child Update Successful", "data": serializer.data,
                             "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)

        return Response({"message": "Child Update Failed", "errors": serializer.errors,
                         "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    
#View for listing all Created children
class ListChild(APIView):
    permission_classes = [IsHealthcareWorker,IsAuthenticated]  # Ensure the user is authenticated
    def get(self, request):
        Child = Child.objects.all()
        serializer = ListChildSerializer(Child, many=True)

        return Response({"message": "Child List Retrieved Successfully", "data": serializer.data,
                         "status": status.HTTP_200_OK})

class DeleteChild(APIView):
    permission_classes = [IsHealthcareWorker,IsAuthenticated]  # Ensure the user is authenticated
    def delete(self, request, child_id, *args, **kwargs):
        try:
            child = Child.objects.get(id=child_id)
            child.delete()
            return Response({"message": "Child Deleted Successfully", "status": status.HTTP_204_NO_CONTENT}, 
                            status=status.HTTP_204_NO_CONTENT)
        except Child.DoesNotExist:
            return Response({"message": "Child not found", "status": status.HTTP_404_NOT_FOUND}, 
                            status=status.HTTP_404_NOT_FOUND)    