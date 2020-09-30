from rest_framework.routers import DefaultRouter
from django.urls import path

from . import views
from . import viewsets

app_name = "rooms"

# router = DefaultRouter()
# router.register("", viewset=viewsets.RoomViewset, basename="room")

# urlpatterns = router.urls


urlpatterns = [
    # path("", views.rooms_view),
    path("", views.RoomsView.as_view()),
    # path("", views.ListRoomsView.as_view()),
    # path("<int:pk>/", views.SeeRoomView.as_view()),
    path("<int:pk>/", views.RoomView.as_view()),
    path("search/", views.room_search),
]
