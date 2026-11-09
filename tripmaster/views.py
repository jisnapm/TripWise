from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from tripmaster.serializers import UserSerializer, TripSerializer
from tripmaster.models import TripDb
from rest_framework import authentication, permissions

# Create your views here.
class SignUpView(APIView):
    def post(self, request):
        form_data = request.data
        s_instance = UserSerializer(data= form_data)
        if s_instance.is_valid():
            s_instance.save()
            return Response(data= s_instance.data, status= 201)
        else:
            return Response(data= s_instance.errors, status= 400)

class UserListCreateView(APIView):
    def get(self, request):
        qs = User.objects.all()
        s_instance = UserSerializer(qs, many= True)
        return Response(data= s_instance.data)
    
class TripListCreateView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = TripDb.objects.all()
        s_instance = TripSerializer(qs, many= True)
        return Response(data= s_instance.data)