import jwt
from django.conf import settings  # Never Never import settings.py directly
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import User
from rooms.models import Room
from .serializers import RelatedUserSerializer, UserSerializer
from rooms.serializers import RoomSerializer


class UsersView(APIView):
    def post(self, request):
        # print(request.data)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            return Response(UserSerializer(new_user).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeView(APIView):

    # Permission classes 를 통해 접근 가능한지 안한지를 알아서 체크 해줌
    # 클래스 전체 메소드에 영향을 줌
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # if request.user.is_authenticated:
        #     return Response(ReadUserSerializer(request.user).data)
        return Response(UserSerializer(request.user).data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
            return Response()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FavsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = RoomSerializer(user.favs.all(), many=True).data
        return Response(serializer)

    def put(self, request):
        pk = request.data.get("pk", None)
        user = request.user
        if pk is not None:
            try:
                room = Room.objects.get(pk=pk)
                if room in user.favs.all():
                    user.favs.remove(room)
                else:
                    user.favs.add(room)
                return Response()
            except Room.DoesNotExist:
                pass
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def user_detail(self, pk):
    try:
        user = User.objects.get(pk=pk)
        return Response(UserSerializer(user).data)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if not username or not password:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if user is not None:
        # You never ever ever ever put secret information to JWT
        # Password, email, username ... 절대 안됨 ! ID 같은 식별자 정도만 !!
        # 토큰은 누구나 볼 수 있다. 그런데 서버는 토큰의 변경 사항을 본다. 토큰안에 어떤 정보가 있는지 상관 안쓴다.
        # 그런데 누구도 건들지 않았다는 여부만 검사한다.
        # 아무도 못보게 만드는게 정보가 아니라, 누군가 건드렸는가 안건드렸는가가 중요한 정보이다.
        encoded_jwt = jwt.encode(
            {"id": user.pk}, settings.SECRET_KEY, algorithm="HS256"
        )
        return Response(data={"token": encoded_jwt})
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    # print(user)


# 두개 이상 처리하는거면 Generic view 써라
# @api_view(["GET", "POST"])
# @permission_classes([IsAuthenticated])
# def toggle_fav(request):
#     room = request.data.get("room")
#     print(room)
#     return Response()