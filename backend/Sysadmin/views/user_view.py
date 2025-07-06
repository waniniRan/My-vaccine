# backend/Sysadmin/views/user_api.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from api.myserializers.user_serializer import UserListSerializer
from Sysadmin.models.User import User

class UserListsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.all()
        data = [
            {
                'id': u.id,
                'username': u.username,
                'email': u.email,
                'role': u.role,
            }
            for u in users
        ]
        return Response(data)