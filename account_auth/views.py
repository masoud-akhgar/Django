from rest_framework import response
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView
from rest_framework.views import APIView
from .serializers import AccountSerializer, TokenSerializer
from .models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token

class Signup(APIView):
    serializer_class = AccountSerializer

    def post(self, request):
        email = ''
        serialized_data = self.serializer_class(data=request.data)
        if serialized_data.is_valid(raise_exception=True): 
            email = serialized_data.data['email']
            password = serialized_data.data['password']

            new_user = User.objects.create_user(email=email, password=password)
        
        return Response(data=
            {
                'message':f"Welcome {email},"
            }
        )

class GetToken(APIView):
    serializer_class = TokenSerializer

    def post(self, request):
        token = None
        serialized_data = self.serializer_class(data=request.data)
        if serialized_data.is_valid(raise_exception=True):  
            email = serialized_data.data['email']
        
        user = User.objects.get(email=email)
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist as t:
            token = Token.objects.create(user=user)
        
        return Response(data=
            {
                'Token': f"{token.key}"
            }
        )


