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

# Using viewset
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from .permissions import IsSelf
from rest_framework.decorators import action


class UsersViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        print(self.action)
        permission_classes = []
        if self.action == "list":
            permission_classes = [IsAdminUser]
        elif (
            self.action == "create"
            or self.action == "retrieve"
            or self.action == "favs"
        ):
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsSelf]
        return [permission() for permission in permission_classes]

    # methods 를 통해 method 한정 지음
    @action(detail=False, methods=["post"])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user is not None:
            encoded_jwt = jwt.encode(
                {"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256"
            )
            return Response(data={"token": encoded_jwt, "pk": user.pk})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True)
    def favs(self, request, pk):
        # request.user의 정보를 받아 오는것이 아닌, pk의 유저의 정보를 받아와야 한다.
        # user = request.user
        # viewset은 지금 detail이 True이기 때문에, 어떤 object를 보고 있는지 알 수 있다.
        # 따라서 get_object()를 하면 현재 보고 있는 object를 반환한다.
        # 그리고 favs 함수는, permission에서 action을 체크해보면 favs가 나오는데, 이에 대한 permission을 따로 처리 해줄 수 있다. ( 비즈니스 로직으로 정하기 나름이다. )
        user = self.get_object()
        serializer = RoomSerializer(user.favs.all(), many=True).data
        return Response(serializer)

    # 커스텀 하고 싶은 메소드를 적으면 됨 ( fav.mapping 다음에 )
    # favs의 put 메소드가 추가 된 것 위에는 기본이라서 get임
    # permission의 action 확인해보면, toggle_favs임 ( 같은 url 이지만, 다른 이름을 가진다. )
    # detail=True 같은건 추가 할 수는 없다. ( 가져만온거 )
    @favs.mapping.put
    def toggle_favs(self, request, pk):
        pk = request.data.get("pk", None)
        # permission에서 보장 받음 따라서 self.get_object() 가능
        user = self.get_object()
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


# class UsersView(APIView):
#     def post(self, request):
#         # print(request.data)
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             new_user = serializer.save()
#             return Response(UserSerializer(new_user).data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class MeView(APIView):

#     # Permission classes 를 통해 접근 가능한지 안한지를 알아서 체크 해줌
#     # 클래스 전체 메소드에 영향을 줌
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         # if request.user.is_authenticated:
#         #     return Response(ReadUserSerializer(request.user).data)
#         return Response(UserSerializer(request.user).data)

#     def put(self, request):
#         serializer = UserSerializer(request.user, data=request.data, partial=True)
#         print(serializer.is_valid())
#         if serializer.is_valid():
#             serializer.save()
#             return Response()
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class FavsView(APIView):

#     permission_classes = [IsAuthenticated]

# def get(self, request):
#     user = request.user
#     serializer = RoomSerializer(user.favs.all(), many=True).data
#     return Response(serializer)

# def put(self, request):
#     pk = request.data.get("pk", None)
#     user = request.user
#     if pk is not None:
#         try:
#             room = Room.objects.get(pk=pk)
#             if room in user.favs.all():
#                 user.favs.remove(room)
#             else:
#                 user.favs.add(room)
#             return Response()
#         except Room.DoesNotExist:
#             pass
#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# @api_view(["GET"])
# def user_detail(self, pk):
#     try:
#         user = User.objects.get(pk=pk)
#         return Response(UserSerializer(user).data)
#     except User.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)


# @api_view(["POST"])
# def login(request):
#     username = request.data.get("username")
#     password = request.data.get("password")
#     if not username or not password:
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#     user = authenticate(username=username, password=password)
#     if user is not None:
#         # You never ever ever ever put secret information to JWT
#         # Password, email, username ... 절대 안됨 ! ID 같은 식별자 정도만 !!
#         # 토큰은 누구나 볼 수 있다. 그런데 서버는 토큰의 변경 사항을 본다. 토큰안에 어떤 정보가 있는지 상관 안쓴다.
#         # 그런데 누구도 건들지 않았다는 여부만 검사한다.
#         # 아무도 못보게 만드는게 정보가 아니라, 누군가 건드렸는가 안건드렸는가가 중요한 정보이다.
#         encoded_jwt = jwt.encode(
#             {"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256"
#         )
#         return Response(data={"token": encoded_jwt})
#     else:
#         return Response(status=status.HTTP_401_UNAUTHORIZED)
#     # print(user)


# 두개 이상 처리하는거면 Generic view 써라
# @api_view(["GET", "POST"])
# @permission_classes([IsAuthenticated])
# def toggle_fav(request):
#     room = request.data.get("room")
#     print(room)
#     return Response()