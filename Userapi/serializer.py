from Stationapi.models import Customer,Train,Booking,Feedback,Payment,Cancellation
from rest_framework import serializers

class CustomerSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    password=serializers.CharField(write_only=True)
    
    class Meta:
        model=Customer
        fields=["id","name","age","email_address","biodata","username","password"]

    def create(self, validated_data):
        return Customer.objects.create_user(**validated_data)
    
class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = "__all__"    


class TicketbookingSerializer(serializers.ModelSerializer):
     user=serializers.CharField(read_only=True)
     train_number=serializers.CharField(read_only=True)
     booking_amount=serializers.CharField(read_only=True)
     class Meta:
        model = Booking
        fields = "__all__"       

class BookingRefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['status']  # Assuming 'status' field is used to track refund status


class FeedbackSerializer(serializers.ModelSerializer):
    customer=serializers.CharField(read_only=True)
    train=serializers.CharField(read_only=True)
    class Meta:
        model = Feedback
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    
    class Meta:
        model=Customer
        fields=["id","name","age","email_address","biodata","username","password"]        

class PaymentSerializer(serializers.ModelSerializer):
    customer=serializers.CharField(read_only=True)
    amount=serializers.CharField(read_only=True)
    class Meta:
        model=Payment
        fields="__all__"    

class CancellationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cancellation
        fields = '__all__'        