from django.urls import path
from rest_framework.routers import DefaultRouter

from TWRL.views import *
from TWRL.viewsets import *

route = DefaultRouter()
route.register('rooms', RoomViewset)
route.register('reservations', ReservationViewset)
route.register('users', UserViewset)

urlpatterns = route.urls

urlpatterns.append(path('room_list/', room_list, name='room_list'))