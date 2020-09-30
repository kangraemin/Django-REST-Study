from rest_framework import serializers
from users.serializers import RelatedUserSerializer
from .models import Room


# class RoomSerializer(serializers.ModelSerializer):

#     user = UserSerializer()

#     class Meta:
#         model = Room
#         exclude = ("modified",)
#         # fields = ("pk", "name", "price", "bedrooms", "user")


class ReadRoomSerializer(serializers.ModelSerializer):

    user = RelatedUserSerializer()

    class Meta:
        model = Room
        exclude = ("modified",)
        # fields = ("pk", "name", "price", "bedrooms", "user")


# User를 create에 받을 수 없다면 ModelSerializer를 안쓰고, 그냥 Serializer를 쓴다. ( ModelSerializer 써도 되는데, 그냥 수동으로 해봄)
class WriteRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        exclude = (
            "user",
            "modified",
            "created",
        )

    def validate(self, data):
        # Create 할때만 적용 되게 할 수 있다.
        if self.instance:
            # default값 부여 가능 ( python의 기능, NOT DRF)
            check_in = data.get("check_in", self.instance.check_in)
            check_out = data.get("check_out", self.instance.check_out)
        else:
            check_in = data.get("check_in")
            check_out = data.get("check_out")
            print(check_in, check_out)
        if check_in == check_out:
            raise serializers.ValidationError("Not enough time between changes")
        return data


# # User를 create에 받을 수 없다면 ModelSerializer를 안쓰고, 그냥 Serializer를 쓴다. ( ModelSerializer 써도 되는데, 그냥 수동으로 해봄)
# class WriteRoomSerializer(serializers.Serializer):

#     name = serializers.CharField(max_length=140)
#     address = serializers.CharField(max_length=140)
#     price = serializers.IntegerField(help_text="USD per night")
#     beds = serializers.IntegerField(default=1)
#     lat = serializers.DecimalField(max_digits=10, decimal_places=6)
#     lng = serializers.DecimalField(max_digits=10, decimal_places=6)
#     bedrooms = serializers.IntegerField(default=1)
#     bathrooms = serializers.IntegerField(default=1)
#     check_in = serializers.TimeField(default="00:00:00")
#     check_out = serializers.TimeField(default="00:00:00")
#     instant_book = serializers.BooleanField(default=False)

#     def create(self, validated_data):
#         print(validated_data)
#         return Room.objects.create(**validated_data)

#     def validate(self, data):
#         # Create 할때만 적용 되게 할 수 있다.
#         if self.instance:
#             # default값 부여 가능 ( python의 기능, NOT DRF)
#             check_in = data.get("check_in", self.instance.check_in)
#             check_out = data.get("check_out", self.instance.check_out)
#         else:
#             check_in = data.get("check_in")
#             check_out = data.get("check_out")
#             print(check_in, check_out)
#         if check_in == check_out:
#             raise serializers.ValidationError("Not enough time between changes")
#         return data

#     def update(self, instance, validated_data):
#         # 모든 데이터를 validated_data로부터 가져오고, 기본 값으로 instance의 값을 사용한다.
#         instance.name = validated_data.get("name", instance.name)
#         instance.address = validated_data.get("address", instance.address)
#         instance.price = validated_data.get("price", instance.price)
#         instance.beds = validated_data.get("beds", instance.beds)
#         instance.lat = validated_data.get("lat", instance.lat)
#         instance.lng = validated_data.get("lng", instance.lng)
#         instance.bedrooms = validated_data.get("bedrooms", instance.bedrooms)
#         instance.bathrooms = validated_data.get("bathrooms", instance.bathrooms)
#         instance.check_in = validated_data.get("check_in", instance.check_in)
#         instance.check_out = validated_data.get("check_out", instance.check_out)
#         instance.instant_book = validated_data.get(
#             "instant_book", instance.instant_book
#         )
#         print(instance, validated_data)
#         instance.save()
#         return instance

# # Django에서의 clean과 비슷함
# def validate_beds(self, beds):
#     if beds < 5:
#         raise serializers.ValidationError("Your house is too small")
#     else:
#         return beds


# class BigRoomSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Room
#         fields = "__all__"
#         exclude = ()

# name = serializers.CharField(max_length=140)
# price = serializers.IntegerField()
# bedrooms = serializers.IntegerField()
# instant_book = serializers.BooleanField()
