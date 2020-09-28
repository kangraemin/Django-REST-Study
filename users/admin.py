from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.User)
class UserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
<<<<<<< HEAD
        ("Custom Profile", {"fields": ("avatar", "superhost",)},),
=======
        ("Custom Profile", {"fields": ("avatar", "superhost", "favs")},),
>>>>>>> 275e68a14aeebd0ddaf92b2d7e7035499f2c4287
    )

    list_display = UserAdmin.list_display + ("room_count",)
