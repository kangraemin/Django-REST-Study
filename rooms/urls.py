from django.urls import path

from . import views

# UsingViewSet
# Viewset create urls automatically we need to connect
# But Search ? -> Extra actions
# https://www.django-rest-framework.org/api-guide/viewsets/#marking-extra-actions-for-routing
# detail이 True라면, -> /rooms/1 처럼 작동
from rest_framework.routers import DefaultRouter

app_name = "rooms"

router = DefaultRouter()
router.register("", viewset=views.RoomViewSet, basename="room")

urlpatterns = router.urls


# urlpatterns = [
# path("", views.rooms_view),
# path("", views.RoomsView.as_view()),
# path("", views.ListRoomsView.as_view()),
# path("<int:pk>/", views.SeeRoomView.as_view()),
# path("<int:pk>/", views.RoomView.as_view()),
# path("search/", views.room_search),
# ]
