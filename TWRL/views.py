from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from TWRL.models import Room
from TWRL.serializers import RoomSerializer


# Create your views here.
@api_view(['GET'])
def room_list(request):
    rooms = Room.objects.all()
    rooms_serializer = RoomSerializer(rooms, many=True)
    return Response(rooms_serializer.data)

@api_view(['GET'])
def logout(request):
	user = request.user
	user.auth_token.delete()
	return Response({"logout":"Logout successfully."})