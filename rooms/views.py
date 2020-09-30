# from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import (
    Response,
)  # Django 의 Response와 다르다 ( Django는 http의 Response )
from rest_framework import status
from .models import Room
from .serializers import ReadRoomSerializer, WriteRoomSerializer


# function based view
# @api_view(["GET", "POST"])
# def rooms_view(request):
#     if request.method == "GET":
#         rooms = Room.objects.all()
#         serializer = ReadRoomSerializer(rooms, many=True).data
#         return Response(serializer)
#     elif request.method == "POST":
#         if not request.user.is_authenticated:
#             return Response(status=status.HTTP_401_UNAUTHORIZED)
#         serializer = WriteRoomSerializer(data=request.data)
#         # print(dir(serializer))
#         # serializer.is_valid() -> Serializer 형태에 안맞는 데이터가 오면, False를 리턴한다. ( 값이 모자란다던지, ... )
#         if serializer.is_valid():
#             # 절대 절대 절대 절대 create 메소드를 바로 부르지 마라 !, save() 메소드를 콜하라 !!!
#             room = serializer.save(user=request.user)
#             room_serializer = ReadRoomSerializer(room).data
#             return Response(data=room_serializer, status=status.HTTP_200_OK)
#         else:
#             # print(serializer.errors)
#             return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 위 function based view와 같음을 인지하라
class RoomsView(APIView):
    def get(self, request):
        rooms = Room.objects.all()
        serializer = ReadRoomSerializer(rooms, many=True).data
        return Response(serializer)

    def post(self, request):
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
            # print(serializer.errors)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ListRoomsView(ListAPIView):
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer

# class SeeRoomView(RetrieveAPIView):

#     queryset = Room.objects.all()
#     serializer_class = ReadRoomSerializer
#     # lookup_url_kwarg = "pkkk" # 기본적으로, url에서 pk라는 이름으로 값을 받는데, 다른 값으로 lookup 해오고 싶을 때 사용 ( url에서 파라메터로 pkkk라는 이름으로 받는 경우임 )

# SeeRoomView를 아래와 같이 변경
class RoomView(APIView):
    def get_room(self, pk):
        try:
            room = Room.objects.get(pk=pk)
            return room
        except Room.DoesNotExist:
            return None

    def get(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            serializer = ReadRoomSerializer(room).data
            return Response(serializer)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            if room.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            # 수정 하고자 한다면, WriteRoomSerializer를 instance로 초기화를 해야한다.
            # 그러면 update를 하려고 한다는걸 인지하게 된다. 따라서 serializer의 create가 아닌 update를 부른다.
            # {
            # "name":"asdf"
            # }
            # Put 을 할 때, 필요한 값을 모두 전송하는것이 아니라면 에러가 뜬다.
            # 하지만, partial = True로 해주면, 부분만 보내도 허용 해준다.
            serializer = WriteRoomSerializer(room, data=request.data, partial=True)
            print(serializer.is_valid(), serializer.errors)
            if serializer.is_valid():
                room = serializer.save()
                return Response(ReadRoomSerializer(room).data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response()
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # Room의 주인인지 아닌지 판단해야한다.
    def delete(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            if room.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            room.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


# class ListRoomsView(APIView):

#     def get(self, request):
#         rooms = Room.objects.all()
#         serializer = RoomSerializer(rooms, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         pass
