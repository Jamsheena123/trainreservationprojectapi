from django.shortcuts import render
from Stationapi.models import Customer,Station,Train,Feedback,TrainCapacity,Refund,Booking
from Stationapi.serializer import StationSerializer,TrainSerializer,FeedbackSerializer,TrainCapacitySerializer,RefundSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework import status
from collections import defaultdict


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

    @action(methods=["post"], detail=True)
    def approve_booking(self, request, *args, **kwargs):
        booking_id = request.data.get("booking_id")
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return Response({"message": "Booking does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user has permission to approve this booking
        if request.user.station != booking.train.station:
            return Response({"message": "You do not have permission to approve this booking."}, status=status.HTTP_403_FORBIDDEN)

        # Update the booking status to 'approved'
        booking.status = "approved"
        booking.save()

        return Response({"message": "Booking approved successfully."}, status=status.HTTP_200_OK)


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

    def list(self, request, *args, **kwargs):
        # Retrieve all train capacities
        qs = TrainCapacity.objects.all()

        # Create a dictionary to store capacities grouped by train number and type
        capacities_by_train_number_and_type = defaultdict(lambda: defaultdict(list))

        # Group capacities by train number and type
        for capacity in qs:
            train_number = capacity.train.train_number  # Accessing train number through foreign key
            train_id = capacity.train_id
            capacities_by_train_number_and_type[train_number][capacity.type].append(capacity.available_seats)

        # Transform the dictionary into a list of dictionaries for serialization
        serialized_data = []
        for train_number, capacities_by_type in capacities_by_train_number_and_type.items():
            # Serialize capacities for each type
            serialized_capacities = [
                {
                    "type": type,
                    "available_seats": sum(seats)  # Summing up available seats for the same type
                }
                for type, seats in capacities_by_type.items()
            ]
            serialized_data.append({
                "train_id": train_id,
                "train_number": train_number,
                "capacities": serialized_capacities
            })

        return Response(data=serialized_data)

 
        
    # def list(self,request,*args,**kwargs):
    #     qs=TrainCapacity.objects.all()
    #     serializer=TrainCapacitySerializer(qs,many=True)
    #     return Response(data=serializer.data)  
    

class RefundView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
        

    def list(self,request,*args,**kwargs):
        qs=Refund.objects.filter(status="pending")
        serializer=RefundSerializer(qs,many=True)
        return Response(data=serializer.data)  
    

    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Refund.objects.get(id=id)
        serializer=RefundSerializer(qs)
        return Response(data=serializer.data)
    
    @action(methods=["post"],detail=True)  
    def refund_approve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Refund.objects.get(id=id)
        qs.status="completed"
        qs.save()
        return Response({'msg':"refund given"})
    







