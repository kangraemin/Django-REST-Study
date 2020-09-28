<<<<<<< HEAD
from django.urls import path

app_name = "users"

urlpatterns = []
=======
from rest_framework.routers import DefaultRouter
from . import views

app_name = "users"

router = DefaultRouter()
router.register("", views.UsersViewSet)
urlpatterns = router.urls
>>>>>>> 275e68a14aeebd0ddaf92b2d7e7035499f2c4287
