from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from tripmaster.serializers import UserSerializer, TripSerializer, TripMemberSerializer
from tripmaster.models import TripDb, TripMemberDb
from rest_framework import authentication, permissions, serializers
from TripWise.permissions import OwnerOnly
from rest_framework.exceptions import PermissionDenied

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
    permission_classes = [OwnerOnly]

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


class TripMemberListCreateView(APIView):
    def get(self, request, trip_id):
        # get trip
        trip_obj = get_object_or_404(TripDb, id=trip_id)
        # 2 Trip to Munnar  Jisna

        is_owner = trip_obj.created_by == request.user
        is_member = TripMemberDb.objects.filter(trip=trip_obj, user=request.user).exists()

        if not (is_owner or is_member):
            raise PermissionDenied("You are not allowed to access this trip")

        members = TripMemberDb.objects.filter(trip=trip_obj)

        s_instance = TripMemberSerializer(members, many=True)

        return Response(data= s_instance.data, status=200)


    def post(self, request, trip_id):
        trip_obj = get_object_or_404(TripDb, id=trip_id)

        if trip_obj.created_by != request.user:
            raise PermissionDenied("Only trip owners can add members")

        form_data = request.data
        s_instance = TripMemberSerializer(data=form_data, context={'trip':trip_obj})

        if s_instance.is_valid():
            s_instance.save()
            return Response(data={'message':'Member added successfully'}, status=201)
        else:
            return Response(data=s_instance.errors)

class TripMemberDeleteView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [OwnerOnly]
    
    def delete(self, request, trip_id, member_id):
        trip_obj = get_object_or_404(TripDb, id=trip_id)

        if trip_obj.created_by != request.user:
            raise PermissionDenied("Only trip owners can delete members")

        member_obj = get_object_or_404(TripMemberDb, id=member_id, trip=trip_obj)
        member_obj.delete()
        return Response(data={'message':'Member deleted successfully'})