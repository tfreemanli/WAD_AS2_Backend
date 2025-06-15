from rest_framework import viewsets
from rest_framework.response import Response
from django.utils.dateparse import parse_datetime
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from TWRL.models import *
from TWRL.serializers import *
from TWRL.permission import *


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated] #[AllowAny, IsAdminUser]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all().order_by('id')
        else:
            return User.objects.filter(id=self.request.user.id).order_by('id')

class ProfileViewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def retrieve(self, request, pk=None):
        # 获取当前用户信息
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)
        
    def list(self, request):
        # 通常我们不希望列出所有用户，所以只返回当前用户信息
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)

class RoomViewset(viewsets.ModelViewSet):
    queryset = Room.objects.all().order_by('room_number')
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

class ReservationViewset(viewsets.ModelViewSet):
    queryset = Reservation.objects.all().order_by('check_in_datetime')
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated] #[IsOwnerOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Reservation.objects.all()
        else:
            return Reservation.objects.filter(Q(client=self.request.user.id) | Q(creator=self.request.user.id))

class MyReservationViewset(viewsets.ModelViewSet):
    queryset = Reservation.objects.all().order_by('check_in_datetime')
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated] #[IsOwnerOrReadOnly]
    def get_queryset(self):
        print(f'Req.user.id = ${self.request.user.id}')
        return Reservation.objects.filter(Q(client=self.request.user.id) | Q(creator=self.request.user.id)).order_by('check_in_datetime')

class PickRoomViewset(viewsets.ModelViewSet):
    queryset = Room.objects.all().order_by('room_number')
    serializer_class = PickRoomSerializer
    permission_classes = [IsAuthenticated]

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['startDT'] = self.request.query_params.get('startDT', '')
        context['endDT'] = self.request.query_params.get('endDT', '')
        return context