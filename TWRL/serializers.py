from rest_framework import serializers

from TWRL.models import Room, Reservation, User


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    client_name = serializers.ReadOnlyField(source='client.first_name') + ' ' + serializers.ReadOnlyField(source='client.last_name')
    creator_name = serializers.ReadOnlyField(source='creator.first_name')
    room_name = serializers.ReadOnlyField(source='room.title')
    class Meta:
        model = Reservation
        fields = ['id', 'created_at', 'updated_at', 'title', 'check_in_datetime', 'check_out_datetime',
         'desc', 'client', 'creator', 'room', 'client_name', 'creator_name', 'room_name']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "email", "first_name", "last_name"]

        extra_kwargs={
            "password": {
                "write_only": True,
                "required": True
            }
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user