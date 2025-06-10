from rest_framework import serializers

from TWRL.models import Room, Reservation


class roomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class reservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'