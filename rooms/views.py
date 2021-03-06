# from rest_framework.views import APIView
# https://www.django-rest-framework.org/api-guide/pagination/
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import (
    Response,
)  # Django 의 Response와 다르다 ( Django는 http의 Response )
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models import Room
from .serializers import RoomSerializer
from .permissions import IsOwner


# Using ViewSet
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

# ModelViewSet은 Create / Retrieve / ... 등의 기능이 미리 탑재 되어 있음
# 누구나 뷰를 수정 할 수 있는 등 로직이 다 사라졌음 -> permission을 이용
# https://www.django-rest-framework.org/api-guide/permissions/
# http://www.cdrf.co/3.9/rest_framework.viewsets/ModelViewSet.html
class RoomViewSet(ModelViewSet):

    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    # See actions
    # https://www.django-rest-framework.org/api-guide/viewsets/#viewset-actions
    def get_permissions(self):

        # /rooms ( GET ) or /room/1 ( GET )
        if self.action == "list" or self.action == "retrieve":
            # Allow any
            permission_classes = [permissions.AllowAny]
        # /room/1 ( PATCH )
        elif self.action == "create":
            permission_classes = [permissions.IsAuthenticated]
        # /room/1 ( DELTE, PUT ) -> Should be isOwner
        # https://www.django-rest-framework.org/api-guide/viewsets/#introspecting-viewset-actions
        else:
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]

    # # http://www.cdrf.co/3.9/rest_framework.viewsets/ModelViewSet.html#get_serializer_context
    # def get_serializer_context(self):
    #     """
    #     Extra context provided to the serializer class.
    #     """
    #     return {"request": self.request, "format": self.format_kwarg, "view": self}

    # action의 이름이 url의 이름
    # url_path 속성으로 url을 바꿀 수 도 있음
    @action(detail=False)
    def search(self, request):
        # paginator = PageNumberPagination()
        # paginator.page_size = 10
        # https://docs.djangoproject.com/en/3.1/topics/db/queries/
        max_price = request.GET.get("max_price", None)
        min_price = request.GET.get("min_price", None)
        beds = request.GET.get("beds", None)
        bedrooms = request.GET.get("bedrooms", None)
        bathrooms = request.GET.get("bathrooms", None)
        lat = request.GET.get("lat", None)
        lng = request.GET.get("lng", None)

        filter_kwargs = {}
        if max_price is not None:
            filter_kwargs["price__lte"] = max_price
        if min_price is not None:
            filter_kwargs["price__gte"] = min_price
        if beds is not None:
            filter_kwargs["beds__gte"] = beds
        if bedrooms is not None:
            filter_kwargs["bedrooms__gte"] = bedrooms
        if bathrooms is not None:
            filter_kwargs["bathrooms__gte"] = bathrooms
        if lat is not None and lng is not None:
            filter_kwargs["lat__gte"] = float(lat) - 0.005
            filter_kwargs["lat__lte"] = float(lat) + 0.005
            filter_kwargs["lng__gte"] = float(lng) - 0.005
            filter_kwargs["lng__lte"] = float(lng) + 0.005

        # {'price__lte': '30', 'bathrooms__gte': '2'}
        print(filter_kwargs)
        # price__lte bathrooms__gte
        print(*filter_kwargs)
        # Print is not work but, price__lte='30', bathrooms__gte='2' 라는 형식으로 줌 따라서 이걸 써야함
        # It (**) is called double expansion / unpacking
        # print(**filter_kwargs)
        # ModelViewSet에는 이미 있는 paginator가 있음, 그걸 사용
        paginator = self.paginator
        try:
            rooms = Room.objects.filter(**filter_kwargs)
        except ValueError:
            rooms = Room.objects.all()
        results = paginator.paginate_queryset(rooms, request)
        serializer = RoomSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)


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


# class OwnPagination(PageNumberPagination):
#     page_size = 20


# # 위 function based view와 같음을 인지하라
# class RoomsView(APIView):
#     def get(self, request):
#         # paginator = PageNumberPagination()
#         # paginator.page_size = 20
#         paginator = OwnPagination()
#         rooms = Room.objects.all()
#         # 모든 방을 가져온 query_set을 paginator에게 parsing 한다. ( parsing -> paginator가 page query argument를 찾아야 한다는 것 )
#         results = paginator.paginate_queryset(rooms, request)
#         serializer = RoomSerializer(results, many=True, context={"request": request})
#         # return paginator.get_paginated_response(serializer.data)를 사용하면, page숫자를 센다던가, 이전 페이지, 다음 페이지 같은 결과값들을 얻을 수 있음
#         # return Response(serializer)
#         return paginator.get_paginated_response(serializer.data)

#     def post(self, request):
#         if not request.user.is_authenticated:
#             return Response(status=status.HTTP_401_UNAUTHORIZED)
#         serializer = RoomSerializer(data=request.data)
#         # print(dir(serializer))
#         # serializer.is_valid() -> Serializer 형태에 안맞는 데이터가 오면, False를 리턴한다. ( 값이 모자란다던지, ... )
#         if serializer.is_valid():
#             # 절대 절대 절대 절대 create 메소드를 바로 부르지 마라 !, save() 메소드를 콜하라 !!!
#             room = serializer.save(user=request.user)
#             room_serializer = RoomSerializer(room).data
#             return Response(data=room_serializer, status=status.HTTP_200_OK)
#         else:
#             # print(serializer.errors)
#             return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ListRoomsView(ListAPIView):
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer

# class SeeRoomView(RetrieveAPIView):

#     queryset = Room.objects.all()
#     serializer_class = ReadRoomSerializer
#     # lookup_url_kwarg = "pkkk" # 기본적으로, url에서 pk라는 이름으로 값을 받는데, 다른 값으로 lookup 해오고 싶을 때 사용 ( url에서 파라메터로 pkkk라는 이름으로 받는 경우임 )

# # SeeRoomView를 아래와 같이 변경
# class RoomView(APIView):
#     def get_room(self, pk):
#         try:
#             room = Room.objects.get(pk=pk)
#             return room
#         except Room.DoesNotExist:
#             return None

#     def get(self, request, pk):
#         room = self.get_room(pk)
#         if room is not None:
#             serializer = RoomSerializer(room).data
#             return Response(serializer)
#         else:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#     def put(self, request, pk):
#         room = self.get_room(pk)
#         if room is not None:
#             if room.user != request.user:
#                 return Response(status=status.HTTP_403_FORBIDDEN)
#             # 수정 하고자 한다면, WriteRoomSerializer를 instance로 초기화를 해야한다.
#             # 그러면 update를 하려고 한다는걸 인지하게 된다. 따라서 serializer의 create가 아닌 update를 부른다.
#             # {
#             # "name":"asdf"
#             # }
#             # Put 을 할 때, 필요한 값을 모두 전송하는것이 아니라면 에러가 뜬다.
#             # 하지만, partial = True로 해주면, 부분만 보내도 허용 해준다.
#             serializer = RoomSerializer(room, data=request.data, partial=True)
#             print(serializer.is_valid(), serializer.errors)
#             if serializer.is_valid():
#                 room = serializer.save()
#                 return Response(RoomSerializer(room).data)
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#             return Response()
#         else:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#     # Room의 주인인지 아닌지 판단해야한다.
#     def delete(self, request, pk):
#         room = self.get_room(pk)
#         if room is not None:
#             if room.user != request.user:
#                 return Response(status=status.HTTP_403_FORBIDDEN)
#             room.delete()
#             return Response(status=status.HTTP_200_OK)
#         else:
#             return Response(status=status.HTTP_404_NOT_FOUND)


# @api_view(["GET"])
# def room_search(request):
#     # paginator = PageNumberPagination()
#     # paginator.page_size = 10
#     # https://docs.djangoproject.com/en/3.1/topics/db/queries/
#     max_price = request.GET.get("max_price", None)
#     min_price = request.GET.get("min_price", None)
#     beds = request.GET.get("beds", None)
#     bedrooms = request.GET.get("bedrooms", None)
#     bathrooms = request.GET.get("bathrooms", None)
#     lat = request.GET.get("lat", None)
#     lng = request.GET.get("lng", None)

#     filter_kwargs = {}
#     if max_price is not None:
#         filter_kwargs["price__lte"] = max_price
#     if min_price is not None:
#         filter_kwargs["price__gte"] = min_price
#     if beds is not None:
#         filter_kwargs["beds__gte"] = beds
#     if bedrooms is not None:
#         filter_kwargs["bedrooms__gte"] = bedrooms
#     if bathrooms is not None:
#         filter_kwargs["bathrooms__gte"] = bathrooms
#     if lat is not None and lng is not None:
#         filter_kwargs["lat__gte"] = float(lat) - 0.005
#         filter_kwargs["lat__lte"] = float(lat) + 0.005
#         filter_kwargs["lng__gte"] = float(lng) - 0.005
#         filter_kwargs["lng__lte"] = float(lng) + 0.005

#     # {'price__lte': '30', 'bathrooms__gte': '2'}
#     print(filter_kwargs)
#     # price__lte bathrooms__gte
#     print(*filter_kwargs)
#     # Print is not work but, price__lte='30', bathrooms__gte='2' 라는 형식으로 줌 따라서 이걸 써야함
#     # It (**) is called double expansion / unpacking
#     # print(**filter_kwargs)
#     paginator = OwnPagination()
#     try:
#         rooms = Room.objects.filter(**filter_kwargs)
#     except ValueError:
#         rooms = Room.objects.all()
#     results = paginator.paginate_queryset(rooms, request)
#     serializer = RoomSerializer(results, many=True)
#     return paginator.get_paginated_response(serializer.data)


# class ListRoomsView(APIView):

#     def get(self, request):
#         rooms = Room.objects.all()
#         serializer = RoomSerializer(rooms, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         pass
