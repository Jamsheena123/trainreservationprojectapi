from  rest_framework import serializers
from Stationapi.models import Customer,Station,Train,Booking,Feedback,TrainCapacity

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


class TrainCapacitySerializer(serializers.ModelSerializer):
    train=serializers.CharField(read_only=True)
    class Meta:
        model = TrainCapacity
        fields = "__all__"

