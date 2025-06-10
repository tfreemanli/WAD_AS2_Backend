from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from TWRL.models import Room
from TWRL.serializers import roomSerializer


# Create your views here.
@api_view(['GET'])
def room_list(request):
    rooms = Room.objects.all()
    rooms_serializer = roomSerializer(rooms, many=True)
    return Response(rooms_serializer.data)