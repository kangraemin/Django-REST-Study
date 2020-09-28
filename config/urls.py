from django.contrib import admin
<<<<<<< HEAD
from django.urls import path
=======
from django.urls import path, include
>>>>>>> 275e68a14aeebd0ddaf92b2d7e7035499f2c4287
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
<<<<<<< HEAD
=======
    path("api/v1/rooms/", include("rooms.urls")),
    path("api/v1/users/", include("users.urls")),
>>>>>>> 275e68a14aeebd0ddaf92b2d7e7035499f2c4287
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
