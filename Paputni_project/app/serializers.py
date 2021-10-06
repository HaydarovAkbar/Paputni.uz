from rest_framework.serializers import ModelSerializer
from .models import *


class PassangerSerializer(ModelSerializer):
    class Meta:
        model = Passenger
        fields = "__all__"


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ("__all__")


class OrderSearchSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "departure_station", "arrival_station", "departure_time")

class PassangerStatusSerializer(ModelSerializer):
    class Meta:
        model = Passenger
        fields = ("id","full_name", "user_status")
