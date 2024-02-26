from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.viewsets import ViewSet,ModelViewSet
from Userapi.serializer import CustomerSerializer,TrainSerializer,TicketbookingSerializer,FeedbackSerializer,ProfileSerializer,PaymentSerializer,CancellationSerializer
from Stationapi.models import Train,Booking,Customer,Cancellation
from django.contrib.auth import logout
from rest_framework import status




class CustomerCreationView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_type="Customer")
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        

class UserProfileView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = request.user.customer.id
        if user_id is None:
            return Response({"error": "Customer profile not found"}, status=404)
        
        qs = Customer.objects.get(id=user_id)
        serializer = CustomerSerializer(qs)
        return Response(data=serializer.data)

    def put(self,request,*args,**kwargs): 
        id=request.user.customer.id
        cus_obj=Customer.objects.get(id=id)
        serializer=ProfileSerializer(data=request.data,instance=cus_obj)
        instance=Customer.objects.get(id=id)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

        
        
import requests  
        
class TrainView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class = TrainSerializer
        
    def list(self,request,*args,**kwargs):
        qs=Train.objects.all()
        serializer=TrainSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Train.objects.get(id=id)
        serializer=TrainSerializer(qs)
        return Response(data=serializer.data)
    
    @action(methods=["post"], detail=True)
    def book_ticket(self, request, *args, **kwargs):
        serializer = TicketbookingSerializer(data=request.data)
        train_id = kwargs.get("pk")
        user_id = request.user.id
        user_obj = Customer.objects.get(id=user_id)
        train_obj = Train.objects.get(id=train_id)
        
        if serializer.is_valid():
            seat_type = serializer.validated_data.get('seat_type')
            reserved_seats = serializer.validated_data.get('reserved_seats')
            amount = self.calculate_amount(train_obj, seat_type, reserved_seats)
            if amount > 0:
                serializer.save(train_number=train_obj, user=user_obj, booking_amount=amount)
                return Response(data=serializer.data)
            else:
                return Response({"error": "Invalid seat type or reserved seats."}, status=400)
        else:
            return Response(data=serializer.errors)

    def calculate_amount(self, train, seat_type, reserved_seats):
        if seat_type == 'Non AC':
            return train.amount_nonac * reserved_seats
        elif seat_type == 'AC':
            return train.amount_ac * reserved_seats
        elif seat_type == 'Sleeper':
            return train.amount_sleeper * reserved_seats
        else:
            return 0


    @action(methods=["post"],detail=True)
    def get_train_livestatus(self,request,*args,**kwargs):
        try:
            id = kwargs.get("pk")
            train_obj = Train.objects.get(id=id)
            train_number = train_obj.train_number
            api_key="af2642c865msh207f12c0e4332a2p1e6979jsnf9ee5c55860d"

            url = f"https://indianrailapi.com/api/v2/livetrainstatus/apikey/{api_key}/trainnumber/{train_number}/date/today"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return Response(data)
            else:
                return Response({"error": "Failed to fetch live train status"}, status=response.status_code)
        except Train.DoesNotExist:
            return Response({"error": "Train not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


    @action(methods=["post"],detail=True)
    def add_feedback(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        object=Train.objects.get(id=id) 
        user=request.user.customer
        serializer=FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(customer=user,train=object)
            return Response(data=serializer.data)
        return Response(data=serializer.errors)   
    
class BookTicketView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=TicketbookingSerializer      
    
    def list(self,request,*args,**kwargs):
        user=request.user.id
        user_obj=Customer.objects.get(id=user)
        qs=Booking.objects.get(user=user_obj)
        serializer=TicketbookingSerializer(qs)
        return Response(data=serializer.data)  
    
      
    def destroy(self, request, *args, **kwargs):
        try:
            id = kwargs.get("pk")
            booking_instance = Booking.objects.get(id=id)
            booking_instance.booking_status = "Cancelled"
            booking_instance.save()
            return Response({"message": "Reservation cancelled successfully"})
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    
    @action(methods=['post'],detail=True)
    def add_payment(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        user=request.user.customer
        id = kwargs.get("pk")
        booking_instance = Booking.objects.get(id=id)
        if booking_instance.booking_status!="cancelled":
            amount=booking_instance.booking_amount
            serializer=PaymentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(customer=user,amount=amount,booking=booking_instance)
                return Response(data=serializer.data)
            return Response(data=serializer.errors)
        else:
            return Response({"error": "Booking already cancelled"}, status=404)




    
def sign_out(request):
    logout(request)
    return render("signin")