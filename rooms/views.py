# from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import (
    Response,
)  # Django 의 Response와 다르다 ( Django는 http의 Response )
from rest_framework import status
from .models import Room
from .serializers import ReadRoomSerializer, WriteRoomSerializer


@api_view(["GET", "POST"])
def rooms_view(request):
    if request.method == "GET":
        rooms = Room.objects.all()
        serializer = ReadRoomSerializer(rooms, many=True).data
        return Response(serializer)
    elif request.method == "POST":
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = WriteRoomSerializer(data=request.data)
        # print(dir(serializer))
        # serializer.is_valid() -> Serializer 형태에 안맞는 데이터가 오면, False를 리턴한다. ( 값이 모자란다던지, ... )
        if serializer.is_valid():
            # 절대 절대 절대 절대 create 메소드를 바로 부르지 마라 !, save() 메소드를 콜하라 !!!
            room = serializer.save(user=request.user)
            room_serializer = ReadRoomSerializer(room).data
            return Response(data=room_serializer, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# class ListRoomsView(ListAPIView):
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer


class SeeRoomView(RetrieveAPIView):

    queryset = Room.objects.all()
    serializer_class = ReadRoomSerializer
    # lookup_url_kwarg = "pkkk" # 기본적으로, url에서 pk라는 이름으로 값을 받는데, 다른 값으로 lookup 해오고 싶을 때 사용 ( url에서 파라메터로 pkkk라는 이름으로 받는 경우임 )


# class ListRoomsView(APIView):

#     def get(self, request):
#         rooms = Room.objects.all()
#         serializer = RoomSerializer(rooms, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         pass
