from django.shortcuts import render
from Stationapi.models import Customer,Station,Train,Feedback,TrainCapacity
from Stationapi.serializer import StationSerializer,TrainSerializer,FeedbackSerializer,TrainCapacitySerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.decorators import action
    

class StationCreationView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=StationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_type="station")
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        

class TrainView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=TrainSerializer

    def create(self,request,*args,**kwargs):
        serializer=TrainSerializer(data=request.data)
        station=request.user.station
        if serializer.is_valid():
            serializer.save(station=station)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
    def list(self,request,*args,**kwargs):
        qs=Train.objects.all()
        serializer=TrainSerializer(qs,many=True)
        return Response(data=serializer.data)
          
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Train.objects.get(id=id)
        serializer=TrainSerializer(qs)
        return Response(data=serializer.data)
   

    def update(self,request,*args,**kwargs):
        serializer=TrainSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
   
    def destroy(self, request, *args, **kwargs):
        id=kwargs.get("pk")
        instance=Train.objects.get(id=id)
        if instance.train==request.customer.train:
            instance.delete()
            return Response(data={"msg":"deleted"})
        else:
            return Response(data={"message":"permission denied"})
        

    @action(methods=["post"],detail=True)
    def add_capacity(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        train_obj=Train.objects.get(id=id) 
        serializer=TrainCapacitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(train=train_obj)
            return Response(data=serializer.data)
        return Response(data=serializer.errors)
        

    @action(methods=["get"],detail=True)  
    def review_list(self,request,*args,**kwargs):
        train_id=kwargs.get("pk")
        train_obj=Train.objects.get(id=train_id)
        qs=Feedback.objects.filter(train=train_id)
        serializer=FeedbackSerializer(qs,many=True)
        return Response(data=serializer.data)

    
class TrainCapacityView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
        
    def list(self,request,*args,**kwargs):
        qs=TrainCapacity.objects.all()
        serializer=TrainCapacitySerializer(qs,many=True)
        return Response(data=serializer.data)  
    






