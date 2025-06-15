from django.urls import path
from rest_framework.routers import DefaultRouter

from TWRL.views import *
from TWRL.viewsets import *

route = DefaultRouter()
route.register('rooms', RoomViewset, basename="rooms")
route.register('reservations', ReservationViewset, basename="managereservations")
route.register('myreservations', MyReservationViewset, basename="myreservations")
route.register('users', UserViewset, basename="manageusers")
route.register('profile', ProfileViewset, basename="profile")
route.register('pickaroom', PickRoomViewset, basename="pickaroom") 


urlpatterns = route.urls

urlpatterns.append(path('room_list/', room_list, name='room_list'))