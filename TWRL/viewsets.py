from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from TWRL.models import *
from TWRL.serializers import *
from TWRL.permission import *


class RoomViewset(viewsets.ModelViewSet):
    queryset = Room.objects.all().order_by('id')
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