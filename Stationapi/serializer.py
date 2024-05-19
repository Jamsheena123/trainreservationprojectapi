from  rest_framework import serializers
from Stationapi.models import Customer,Station,Train,Booking,Feedback,TrainCapacity,Refund
from Userapi.serializer import CustomerSerializer

class StationSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    password=serializers.CharField(write_only=True)

    class Meta:
        model=Station
        fields=["id","name","phone_number","username","password","station_code","Location"]


    def create(self,validated_data):
        return Station.objects.create_user(**validated_data)
    

class TrainSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    station=serializers.CharField(read_only=True)
    class Meta:
        model = Train
        fields = ['id','train_name', 'train_number', 'source', 'destination', 'departure_time', 'arrival_time',"amount_nonac","amount_ac","amount_sleeper","station" ]      



class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"


# class TrainCapacitySerializer(serializers.ModelSerializer):
#     train=serializers.CharField(read_only=True)

#     class Meta:
#         model = TrainCapacity
#         fields = "__all__"

class TrainCapacitySerializer(serializers.ModelSerializer):
    train_number = serializers.CharField(source='train.train_number', read_only=True)

    class Meta:
        model = TrainCapacity
        fields = ['train_number', 'type', 'available_seats']


class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = "__all__"
        
        
class TicketBookingViewSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(source='user', read_only=True)  # Assuming 'user' is the ForeignKey to Customer
    train = TrainSerializer(read_only=True)  # Assuming 'train' is the ForeignKey to Train

    class Meta:
        model = Booking
        fields = ['id', 'train', 'customer', 'booking_time', 'seat_type', 'reserved_seats', 'reservation_date', 'booking_amount', 'booking_status']