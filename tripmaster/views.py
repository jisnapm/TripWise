from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from tripmaster.serializers import UserSerializer, TripSerializer
from tripmaster.models import TripDb
from rest_framework import authentication, permissions, serializers

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

class UserRetreiveUpdateDeleteView(APIView):
    def get(self, request, pk):
        qs = get_object_or_404(User, id= pk)
        s_instance = UserSerializer(qs)
        return Response(data= s_instance.data)

    def delete(self, request, pk):
        qs = get_object_or_404(User, id= pk)
        qs.delete()
        return Response(data= {"message": "User Deleted Successfully!"})
    
class TripListCreateView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = TripDb.objects.filter(created_by= request.user)
        s_instance = TripSerializer(qs, many= True)
        return Response(data= s_instance.data)

    def post(self, request):
        form_data = request.data
        s_instance = TripSerializer(data= form_data)
        if s_instance.is_valid():
            s_instance.save(created_by= request.user)
            return Response(data= {"message": "Trip Created Successfully!",
                                   "your trip details":s_instance.data}, status= 201)
        else:
            return Response(data= s_instance.errors, status= 400)


class TripRetreiveUpdateDeleteView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        trip_object = get_object_or_404(TripDb, id= pk)
        if trip_object.created_by == request.user:
            s_instance = TripSerializer(trip_object)
            return Response(data= s_instance.data)
        else:
            raise serializers.ValidationError("Access Denied!")

    def put(self, request, pk):
        trip_object = get_object_or_404(TripDb, id= pk)
        if trip_object.created_by != request.user:
            raise serializers.ValidationError("Access Denied!")
        form_data = request.data
        s_instance = TripSerializer(data= form_data, instance= trip_object)
        if s_instance.is_valid():
            s_instance.save()
            return Response(data= {"message": "Trip Updated Successfully!",
                                   "updated trip details":s_instance.data}, status= 201)
        else:
            return Response(data= s_instance.errors)
        
    def delete(self, request, pk):
        trip_object = get_object_or_404(TripDb, id= pk)
        if trip_object.created_by != request.user:
            raise serializers.ValidationError("Access Denied!")
        trip_object.delete()
        return Response(data= {"message": "Trip Deleted Successfully!"})
