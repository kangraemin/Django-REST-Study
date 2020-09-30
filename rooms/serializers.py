from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Room


# class RoomSerializer(serializers.ModelSerializer):

#     user = UserSerializer()

#     class Meta:
#         model = Room
#         exclude = ("modified",)
#         # fields = ("pk", "name", "price", "bedrooms", "user")


class ReadRoomSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Room
        exclude = ("modified",)
        # fields = ("pk", "name", "price", "bedrooms", "user")


# User를 create에 받을 수 없다면 ModelSerializer를 안쓰고, 그냥 Serializer를 쓴다. ( ModelSerializer 써도 되는데, 그냥 수동으로 해봄)
class WriteRoomSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=140)
    address = serializers.CharField(max_length=140)
    price = serializers.IntegerField(help_text="USD per night")
    beds = serializers.IntegerField(default=1)
    lat = serializers.DecimalField(max_digits=10, decimal_places=6)
    lng = serializers.DecimalField(max_digits=10, decimal_places=6)
    bedrooms = serializers.IntegerField(default=1)
    bathrooms = serializers.IntegerField(default=1)
    check_in = serializers.TimeField(default="00:00:00")
    check_out = serializers.TimeField(default="00:00:00")
    instant_book = serializers.BooleanField(default=False)

    def create(self, validated_data):
        print(validated_data)
        return Room.objects.create(**validated_data)


# class BigRoomSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Room
#         fields = "__all__"
#         exclude = ()

# name = serializers.CharField(max_length=140)
# price = serializers.IntegerField()
# bedrooms = serializers.IntegerField()
# instant_book = serializers.BooleanField()
