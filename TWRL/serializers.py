from rest_framework import serializers

from TWRL.models import Room, Reservation, User


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    client_fname = serializers.ReadOnlyField(source='client.first_name')
    client_lname = serializers.ReadOnlyField(source='client.last_name')
    creator_fname = serializers.ReadOnlyField(source='creator.first_name')
    creator_lname = serializers.ReadOnlyField(source='creator.last_name')
    room_name = serializers.ReadOnlyField(source='room.title')
    class Meta:
        model = Reservation
        fields = ['id', 'created_at', 'updated_at', 'title', 'check_in_datetime', 'check_out_datetime',
         'desc', 'client', 'creator', 'room', 'client_fname', 'client_lname', 'creator_fname', 'creator_lname', 'room_name']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "email", "first_name", "last_name","is_staff"]

        extra_kwargs={
            "password": {
                "write_only": True,
                "required": False  # 不是必填
            }
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        # 更新时密码是可选的
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "is_staff"]

class PickRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'