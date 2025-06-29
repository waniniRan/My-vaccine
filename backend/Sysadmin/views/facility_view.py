from rest_framework.views import APIView
from api.myserializers.facility_serializer import CreateHealthFacilitySerializer
from rest_framework.response import Response
from rest_framework import status

class CreateHealthFacility(APIView):

   def post(self, request, *args, **kwargs):
      serializer = CreateHealthFacilitySerializer(data=request.data, context={'request': request})
         
      if serializer.is_valid(): 
         serializer.save()

         return Response( {"message": "Blog Post Creation Successful", "data": serializer.data,
                         "status": status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)

      return Response({"message": "Health Facility Creation Failed", "errors": serializer.errors,
                         "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)  
