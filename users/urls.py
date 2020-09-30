from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("", views.UsersView.as_view()),
    path("me/", views.MeView.as_view()),
    path("me/favs/", views.FavsView.as_view()),
    # path("me/favs/", views.toggle_fav),
    path("<int:pk>", views.user_detail),
    path("token/", views.login),
]
