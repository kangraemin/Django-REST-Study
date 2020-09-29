# from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from .models import Room
from .serializers import RoomSerializer


class ListRoomsView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class SeeRoomView(RetrieveAPIView):

    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    # lookup_url_kwarg = "pkkk" # 기본적으로, url에서 pk라는 이름으로 값을 받는데, 다른 값으로 lookup 해오고 싶을 때 사용 ( url에서 파라메터로 pkkk라는 이름으로 받는 경우임 )


# class ListRoomsView(APIView):

#     def get(self, request):
#         rooms = Room.objects.all()
#         serializer = RoomSerializer(rooms, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         pass
