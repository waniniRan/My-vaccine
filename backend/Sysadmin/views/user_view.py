# backend/Sysadmin/views/user_api.py
from rest_framework.views import APIView
from rest_framework.response import Response
from api.myserializers.user_serializer import UserListSerializer
from Sysadmin.models.User import User
from Sysadmin.views.permissions import IsSystemAdmin
from rest_framework.permissions import IsAuthenticated

class UserListsView(APIView):
    permission_classes = [IsAuthenticated ,IsSystemAdmin]  # Ensure only system admins can access this view

    def get(self, request):
        users = User.objects.all()
        if not users.exists():
            return Response({'data': []}, status=200)
        serializer = UserListSerializer(users, many=True)
        return Response({'data': serializer.data}, status=200)