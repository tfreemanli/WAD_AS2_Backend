from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from TWRL.models import *
from TWRL.serializers import *
from TWRL.permission import *


class RoomViewset(viewsets.ModelViewSet):
    queryset = Room.objects.all().order_by('room_number')
    serializer_class = RoomSerializer
    permission_classes = [AllowAny]

class ReservationViewset(viewsets.ModelViewSet):
    queryset = Reservation.objects.all().order_by('check_in_datetime')
    serializer_class = ReservationSerializer
    permission_classes = [AllowAny] #[IsOwnerOrReadOnly]

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [AllowAny] #[IsAuthenticated, IsAdminUser]

    # def get_queryset(self):
    #     if self.request.user.is_superuser:
    #         return User.objects.all()
    #     else:
    #         return User.objects.filter(id=self.request.user.id)

class PickRoomViewset(viewsets.ModelViewSet):
    queryset = Room.objects.all().order_by('room_number')
    serializer_class = PickRoomSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        
        queryset = Room.objects.all().order_by('room_number')
        startDT = self.request.query_params.get('startDT')
        endDT = self.request.query_params.get('endDT')

        if startDT and endDT:
            try:
                startDT = parse_datetime(startDT)
                endDT = parse_datetime(endDT)

                if startDT and endDT:
                    reserved_rooms = Reservation.objects.filter(
                        Q(check_in_datetime__lt=endDT) & Q(check_out_datetime__gt=startDT)
                    ).values_list('room_id', flat=True)

                    queryset = queryset.exclude(id__in=reserved_rooms)
            except ValueError:
                pass

        return queryset