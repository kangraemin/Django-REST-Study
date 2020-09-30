from rest_framework import serializers
from .models import User


class RelatedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "avatar",
            "superhost",
        )
        # fields = ("username", "superhost")


class ReadUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "groups",
            "user_permissions",
            "password",
            "last_login",
            "is_superuser",
            "is_staff",
            "is_active",
            "date_joined",
            "favs",
        )


# Serializer는 왠만하면 상속해서 쓰는것이 편하다.
# View는 그렇지 않은 경우도 많다.
class WriteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
        )

    def validate_first_name(self, value):
        print(value)
        return value.upper()
