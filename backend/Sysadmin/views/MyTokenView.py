from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from api.myserializers.MyTokenSerializer import MyTokenSerializer


class MyTokenView(TokenObtainPairView):
    serializer_class = MyTokenSerializer