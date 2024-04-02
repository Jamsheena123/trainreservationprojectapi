from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.viewsets import ViewSet,ModelViewSet
from Userapi.serializer import CustomerSerializer,TrainSerializer,TicketbookingSerializer,FeedbackSerializer,ProfileSerializer,PaymentSerializer,CancellationSerializer,TrainStatusSerializer,TrainCapacitySerializer,TicketbookingViewSerializer,RefundSerializer
from Stationapi.models import Train,Booking,Customer,Cancellation,Payment,Refund,TrainCapacity,Feedback
from django.contrib.auth import logout
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Sum
from datetime import datetime
from rest_framework.permissions import AllowAny
import json








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
   
 
    def list(self, request, *args, **kwargs):
        qs = Train.objects.all()
        serializer = TrainSerializer(qs, many=True)
        for train_data in serializer.data:
            train_capacity = Train.objects.filter(id=train_data['id']).values('traincapacity__type', 'traincapacity__available_seats')
            train_data['train_capacity'] = train_capacity
        return Response(serializer.data)
    

    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Train.objects.get(id=id)
        serializer=TrainSerializer(qs)
        return Response(data=serializer.data)
    

    @action(methods=['post'],detail=True)
    def check_availability(self, request, *args, **kwargs):
        train_id = kwargs.get("pk")
        seat_type = request.data.get("type")

        try:
            train = Train.objects.get(id=train_id)
            capacity = TrainCapacity.objects.get(train=train, type=seat_type)  # Use 'type' instead of 'seat_type'
            return Response({"available_seats": capacity.available_seats}, status=status.HTTP_200_OK)
        except Train.DoesNotExist:
            return Response({"message": "Train not found"}, status=status.HTTP_404_NOT_FOUND)
        except TrainCapacity.DoesNotExist:
            return Response({"message": f"No capacity information found for {seat_type} seats in this train"},
                            status=status.HTTP_404_NOT_FOUND)




        


    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
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

            # Check if requested number of seats are available
            if self.check_available_seats(train_obj, seat_type, reserved_seats):
                amount = self.calculate_amount(train_obj, seat_type, reserved_seats)
                if amount > 0:
                    # Deduct reserved seats from capacity
                    self.update_seat_capacity(train_obj, seat_type, reserved_seats)
                    serializer.save(train_number=train_obj, user=user_obj, booking_amount=amount)
                    return Response(data=serializer.data)
                else:
                    return Response({"error": "Invalid seat type or reserved seats."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Requested seats are not available."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   
   
    def check_available_seats(self, train, seat_type, reserved_seats):
        try:
            train_capacity = TrainCapacity.objects.get(train=train, type=seat_type)
            return train_capacity.available_seats >= reserved_seats
        except TrainCapacity.DoesNotExist:
            return False

    def update_seat_capacity(self, train, seat_type, reserved_seats):
        try:
            train_capacity = TrainCapacity.objects.get(train=train, type=seat_type)
            train_capacity.available_seats -= reserved_seats
            train_capacity.save()
        except TrainCapacity.DoesNotExist:
            pass

    def calculate_amount(self, train, seat_type, reserved_seats):
        if seat_type == 'Non AC':
            return train.amount_nonac * reserved_seats
        elif seat_type == 'AC':
            return train.amount_ac * reserved_seats
        elif seat_type == 'Sleeper':
            return train.amount_sleeper * reserved_seats
        else:
            return 0
        
    

        

    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    @action(methods=["post"], detail=True)
    def add_feedback(self, request, *args, **kwargs):
        train_id = kwargs.get("pk")
        train_object = Train.objects.get(id=train_id)
        user = request.user.customer
        existing_feedback =Feedback.objects.filter(train=train_object, customer=user).first()
        if existing_feedback:
            return Response({"message": "Feedback already added for this train"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(customer=user, train=train_object)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
class BookTicketView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
     
    
    def list(self, request, *args, **kwargs):
        user_id = request.user.id
        try:
            user_obj = Customer.objects.get(id=user_id)
            bookings = Booking.objects.filter(user=user_obj)
            if bookings.exists():
                serializer = TicketbookingViewSerializer(bookings, many=True)
                return Response(serializer.data)
            else:
                return Response({"message": "No bookings found for the user"}, status=status.HTTP_404_NOT_FOUND)
        except Customer.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Booking.MultipleObjectsReturned:
            return Response({"error": "Multiple bookings found for the same user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

      
    # def destroy(self, request, *args, **kwargs):
    #     try:
    #         id = kwargs.get("pk")
    #         booking_instance = Booking.objects.get(id=id)
    #         booking_instance.booking_status = "Cancelled"
    #         booking_instance.save()
    #         return Response({"message": "Reservation cancelled successfully"})
    #     except Booking.DoesNotExist:
    #         return Response({"error": "Booking not found"}, status=404)
    #     except Exception as e:
    #         return Response({"error": str(e)}, status=500)

    @action(methods=['post'],detail=True)
    def add_payment(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        user=request.user.customer
        id = kwargs.get("pk")
        booking_instance = Booking.objects.get(id=id)
        if booking_instance.booking_status!="Cancelled":
            amount=booking_instance.booking_amount
            request.data["status"] = "completed" 
            serializer=PaymentSerializer(data=request.data)
            if serializer.is_valid():
                booking_instance.booking_status="Completed"
                booking_instance.save()
                serializer.save(customer=user,amount=amount,booking=booking_instance)
                return Response(data=serializer.data)
            return Response(data=serializer.errors)
        else:
            return Response({"error": "Booking already cancelled"}, status=404)
        

    @action(methods=['post'], detail=True)
    def cancel_and_refund(self, request, *args, **kwargs):
        try:
            booking_id = kwargs.get("pk")
            booking_instance = Booking.objects.get(id=booking_id)

            if booking_instance.booking_status == "Cancelled":
                return Response({"error": "Booking is already cancelled"}, status=status.HTTP_400_BAD_REQUEST)

            # Cancel Booking
            booking_instance.booking_status = "Cancelled"
            booking_instance.save()

            # Create Refund
            refund_amount = booking_instance.booking_amount
            refund = Refund.objects.create(
                status='pending',
                booking=booking_instance,
                customer=booking_instance.user,
                amount=refund_amount
            )

            return Response({
                "message": "Booking cancelled and refund initiated successfully",
                "refund_id": refund.id,
                "customer_name": refund.customer.name,
                "refund_amount": refund.amount,
                "booking_id": refund.booking.id
            })

        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   





    # @action(methods=['post'], detail=True)
    # def refund_ticket(self, request, *args, **kwargs):
    #     try:
    #         booking_id = kwargs.get("pk")
    #         booking_instance = Booking.objects.get(id=booking_id)

    #         if booking_instance.booking_status == "Cancelled":
    #             # Check if refund already exists for this booking
    #             if Refund.objects.filter(booking=booking_instance).exists():
    #                 return Response({"error": "Refund already processed for this booking"}, status=status.HTTP_400_BAD_REQUEST)
                
    #             refund_amount = booking_instance.booking_amount
    #             refund = Refund.objects.create(
    #                 status='pending',
    #                 booking=booking_instance,
    #                 customer=booking_instance.user,
    #                 amount=refund_amount
    #             )

    #             return Response({"message": "Refund initiated successfully", "refund_id": refund.id, 'customer_name': refund.customer.name, 'refund_amount': refund.amount, 'booking_id': refund.booking.id})
    #         else:
    #             return Response({"error": "Booking is not cancelled, refund cannot be processed"}, status=status.HTTP_400_BAD_REQUEST)
    #     except Booking.DoesNotExist:
    #         return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)
    #     except Exception as e:
    #         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
def search_trains_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            search_term = data.get('search')
            if search_term:
                url = "https://trains.p.rapidapi.com/"
                payload = {"search": search_term}
                headers = {
                    "content-type": "application/json",
                    "X-RapidAPI-Key": "ecaa2bd736msh28cbeae8e944acfp161787jsncfbeabcf9622",
                    "X-RapidAPI-Host": "trains.p.rapidapi.com"
                }
                response = requests.post(url, json=payload, headers=headers)
                response.raise_for_status()  # Raise an exception for bad status codes
                return JsonResponse(response.json(), safe=False)
            else:
                return JsonResponse({"error": "Search term is missing"}, status=400)
        except json.JSONDecodeError as e:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)



def search_train(request):
    if request.method == 'POST':
        source = request.POST.get('source')
        destination = request.POST.get('destination')
        date_str = request.POST.get('date')
        query = Train.objects.all()
        if source:
            query = query.filter(source=source)
        if destination:
            query = query.filter(destination=destination)
        if date_str:
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
                query = query.filter(departure_time__date=date)
            except ValueError:
                return JsonResponse({'error': 'Invalid date format. Please use YYYY-MM-DD.'}, status=400)
        trains = query
        train_list = []
        for train in trains:
            train_info = {
                'train_name': train.train_name,
                'train_number': train.train_number,
                'departure_time': train.departure_time.strftime('%Y-%m-%d %H:%M:%S'),
                'arrival_time': train.arrival_time.strftime('%Y-%m-%d %H:%M:%S'),
                'amount_nonac': train.amount_nonac,
                'amount_ac': train.amount_ac,
                'amount_sleeper': train.amount_sleeper,
            }
            train_list.append(train_info)
        return JsonResponse({'trains': train_list})
    return JsonResponse({'error': 'Invalid request method'}, status=405)
search_train.permission_classes = [AllowAny]



class RefundView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
        

    def list(self,request,*args,**kwargs):
        user=request.user.customer
        qs=Refund.objects.filter(customer=user)
        serializer=RefundSerializer(qs,many=True)
        return Response(data=serializer.data)
          
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Refund.objects.get(id=id)
        serializer=RefundSerializer(qs)
        return Response(data=serializer.data)