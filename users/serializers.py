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


# class ReadUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         exclude = (
#             "groups",
#             "user_permissions",
#             "password",
#             "last_login",
#             "is_superuser",
#             "is_staff",
#             "is_active",
#             "date_joined",
#             "favs",
#         )


# Serializer는 왠만하면 상속해서 쓰는것이 편하다.
# View는 그렇지 않은 경우도 많다.
# class WriteUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = (
#             "username",
#             "first_name",
#             "last_name",
#             "email",
#         )

#     def validate_first_name(self, value):
#         print(value)
#         return value.upper()


class UserSerializer(serializers.ModelSerializer):

    # write_only -> 이건 표시 되지 않는다.
    # Write 할 수 있고, Recevie 할 수 있지만, 보여주지는 않을거다.
    password = serializers.CharField(write_only=True)

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
            "password",
        )
        read_only_fields = ("id", "superhost", "avatar")

    def validate_first_name(self, value):
        print(value)
        return value.upper()

    def create(self, validated_data):
        # fields에 password를 적으면, get에서 보이는데 이를 피하기 위해 적지 않았다. 따라서 validated_data에 password는 오지 않는다.
        # 그런데 user 회원가입 위해선 받아야 한다. 따라서 write_only 옵션을 넣는다.
        # print(validated_data)

        # password는 set_password를 통해서 넣어야한다.
        password = validated_data.get("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user
